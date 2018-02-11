#!/usr/bin/python3.5

import argparse
import email
import getpass
import imaplib
import os
import re
import sys
import zipfile
from imaplib import IMAP4
from pathlib import Path

parser = argparse.ArgumentParser(description='Backupboy a backup log interpreter.')
parser._action_groups.pop()

rargs = parser.add_argument_group('required arguments')
oargs = parser.add_argument_group('optional arguments')

rargs.add_argument('--server', metavar='SERVER', type=str,
                   help='Imap server. "imap.mailserver.com"', required=True)
rargs.add_argument('--user', metavar='Username', type=str,
                   help='Imap user', required=True)
rargs.add_argument('--software', metavar='Name', type=str,
                   help='Software target {backupexec_en-us, backupexec_pt-br, cobian, robocopy_en-us, robocopy_pt-br}',
                   required=True,
                   choices=['backupexec_en-us', 'backupexec_pt-br', 'backupexec_pt', 'cobian',
                            'robocopy_en-us',
                            'robocopy_pt-br'])
rargs.add_argument('--subject', metavar='Subject', type=str,
                   help='Mail subject text. "Some other subject"', required=True)

oargs.add_argument('--port', metavar='143', type=int,
                   help='Imap server port. Default=143', default=143)
oargs.add_argument('--index', metavar='CSV Index', type=str,
                   help='The first csv collumn')
oargs.add_argument('--folder', metavar='INBOX', type=str,
                   help='The imap target folder "INBOX/Backup XYZ". Default="INBOX"', default="INBOX")
oargs.add_argument('--since', metavar='01-Apr-2018', type=str,
                   help='Mails since date')
oargs.add_argument('--sender', metavar='Name', type=str,
                   help='Mail sender name. "The BackupBoy"')
oargs.add_argument('--jobname', metavar='DailyJob', type=str,
                   help='Custom job name. Combined with --software robocopy_[*]')
oargs.add_argument('--force', default=False, action='store_true',
                   help='Ignore invalid logs.')
oargs.add_argument('--ssl', default=False, action='store_true',
                   help='Use ssl encrypted connection.')
oargs.add_argument('--tls', default=False, action='store_true',
                   help='Use tls encrypted connection.')
oargs.add_argument('--password', metavar='Password', type=str,
                   help='Imap password.')

args = parser.parse_args()

criteria = "SUBJECT \"{}\"".format(args.subject)

if args.since:
    criteria = "{} SINCE \"{}\"".format(criteria, args.since)
if args.sender:
    criteria = "{} FROM \"{}\"".format(criteria, args.sender)

if args.ssl:
    imap = imaplib.IMAP4_SSL(args.server, args.port)
else:
    imap = IMAP4(args.server, args.port)

if args.tls:
    imap.starttls()

if args.password:
    password = args.password
else:
    password = getpass.getpass()

imap.login(args.user, password)

try:
    imap.select(imap._quote(args.folder), True)
    data = imap.search(None, criteria)
except UnicodeEncodeError:
    print("Error: invalid chars on IMAP.")
    sys.exit(1)

try:
    os.mkdir("logs")
except FileExistsError:
    pass

for id in data[1][0].split():
    err, mail_parts = imap.fetch(id, '(RFC822)')
    mail_body = mail_parts[0][1]
    mail = email.message_from_bytes(mail_body)

    for mail_part in mail.walk():
        if mail_part.get_content_maintype() == 'multipart':
            # print(mail_part.as_string())
            continue
        if mail_part.get('Content-Disposition') is None:
            # print(mail_part.as_string())
            continue
        mail_attachment_name = mail_part.get_filename()
        if bool(mail_attachment_name):
            filePath = os.path.join('.', 'logs', mail_attachment_name)
            if not os.path.isfile(filePath):
                fp = open(filePath, 'wb')
                fp.write(mail_part.get_payload(decode=True))
                fp.close()

                if args.software.split('_')[0] == "backupexec":
                    fileContent = Path(filePath).read_text("UTF-16 LE")
                    if args.software.split('_')[1] == "en-us":
                        job_name = re.findall('Job name: ([^\n|<]*)', fileContent)
                        job_start = re.findall('Job started: ([^\n|<]*)', fileContent)
                        job_end = re.findall('Job ended: ([^<|\n]*)', fileContent)
                        job_status = re.findall('Completed status: ([^\n|<]*)', fileContent)
                    elif args.software.split('_')[1] == "pt-br":
                        job_name = re.findall('Nome da tarefa: ([^\n|<]*)', fileContent)
                        job_start = re.findall('Tarefa iniciada: ([^\n|<]*)', fileContent)
                        job_end = re.findall('Tarefa finalizada: ([^<|\n]*)', fileContent)
                        job_status = re.findall('Status de conclusão: ([^\n|<]*)', fileContent)
                    elif args.software.split('_')[1] == "pt":
                        job_name = re.findall('Nome do trabalho: ([^\n|<]*)', fileContent)
                        job_start = re.findall('Tarefa iniciada: ([^\n|<]*)', fileContent)
                        job_end = re.findall('Tarefa finalizada: ([^<|\n]*)', fileContent)
                        job_status = re.findall('Status de conclusão: ([^\n|<]*)', fileContent)
                    try:
                        if args.index:
                            print("{};{};{};{};{}".format(args.index, job_name[0], job_start[0], job_end[0],
                                                          job_status[0]))
                        else:
                            print("{};{};{};{}".format(job_name[0], job_start[0], job_end[0], job_status[0]))
                    except IndexError:
                        if args.force:
                            pass
                        else:
                            print("Error: Wrong log content.")
                            sys.exit(1)
                elif args.software == "cobian":
                    dir = os.path.dirname(filePath)
                    file = zipfile.ZipFile(filePath)
                    log = file.namelist()[0]
                    zipfile.ZipFile(filePath).extract(log, dir)
                    fileContent = Path(dir + os.sep + log).read_text("UTF-16 LE")
                    os.remove(dir + os.sep + log)
                    match = re.findall(
                        '^\s{4}([^\s]* [^\s]*) \*{2} [^\"]*\"([^\"]*)\" \*{2}[^\*]*\*{2}[^\:]*\S\s([\d]*)\.[^\.]*\.[^\.]*\.[^\:]*\:\s([^\s]*\s[\w]*)[^\d]*([^\s]* [^\s]*) -{2}',
                        fileContent, re.MULTILINE)
                    for line in match:
                        if args.index:
                            print(
                                "{};{};{};{};{};{}".format(args.index, line[1], line[0], line[4], line[2], line[3]))
                        else:
                            print("{};{};{};{};{}".format(line[1], line[0], line[4], line[2], line[3]))
                elif args.software.split('_')[0] == "robocopy":
                    dir = os.path.dirname(filePath)
                    file = zipfile.ZipFile(filePath)
                    log = file.namelist()[0]
                    zipfile.ZipFile(filePath).extract(log, dir)
                    fileContent = Path(dir + os.sep + log).read_text("ISO-8859-1")
                    os.remove(dir + os.sep + log)
                    if args.software.split('_')[1] == "en-us":
                        job_start = re.findall('Started : ([^\n]*)', fileContent)
                        job_end = re.findall('Ended : ([^\n]*)', fileContent)
                        job_status = len(re.findall('\(0x[0-9a-zA-Z]{8}\)', fileContent))
                    elif args.software.split('_')[1] == "pt-br":
                        job_start = re.findall('Iniciado: ([^\n]*)', fileContent)
                        job_end = re.findall('Finalizado em: ([^\n]*)', fileContent)
                        job_status = len(re.findall('\(0x[0-9a-zA-Z]{8}\)', fileContent))
                    try:
                        if args.index:
                            print("{};{};{};{};{}".format(args.index, args.jobname, job_start[0], job_end[-1],
                                                          job_status))
                        else:
                            print("{};{};{};{}".format(args.jobname, job_start[0], job_end[-1],
                                                       job_status))
                    except IndexError:
                        if args.force:
                            pass
                        else:
                            print("Error: Wrong log content.")
                            sys.exit(1)
            os.remove(filePath)
imap.logout()
