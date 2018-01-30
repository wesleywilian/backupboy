# backupboy

> [Readme in English](README.md)


> [Readme in Portuguese](README_PT-BR.md)


### 1. Introduction
Backup softwares are great tools in an infrastructure, not just in the corporate context, but also in the individual context.

However, at a time when there are hundreds of backup software as well as many backup jobs, it is costly to manage the results of these backup jobs, hampering the identification of problems and their correct functioning.

**Backupboy** is a project whose purpose is to solve the above problem by interpreting the logs of various software in different languages.

### 2. Operation
**Backupboy** is a project written in Python which downloads the logs from email using the IMAP protocol, decompress the file if necessary and captures relevant information to generate an objective output of the backup job state.

#### 2.1 Supported Software
- Cobian Backup 11
- Backup Exec
- Robocopy

#### 2.2 Compatibility

Below, the table describes Backupboy's current compatibility.

|Software|Job name|Job start time|Job end time|Job status|Data volume|
|-|-|-|-|-|-|
|Cobian Backup 11|Compatible|Compatible|Compatible|Capture the amount of errors on job|Compatible|
|Backup Exec|Compatible|Compatible|Compatible|Capture the job status|-|
|Robocopy|Informed by argument --jobname|Compatible|Compatible|Capture the amount of errors on job|-|

#### 2.3 Language

Below, the currently supported languages.

|Software|Language|
|-|-|
|Cobian Backup 11|Inglês|
|Cobian Backup 11|Portuguese Brazil|
|Backup Exec|Inglês|
|Backup Exec|Portuguese Brazil|
|Robocopy|Inglês|
|Robocopy|Portuguese Brazil|

#### 2.4 Available Outputs
- CSV: Output format that uses a key character to delimit the data content.

### 3. Use
To use Backupboy you must have access and valid credentials on an IMAP server, use Python 3.5 in a Linux environment.

### 3.1 Running without arguments
Here is an example of running without informed arguments.

```sh
wesley@pyhost:~$ ./backupboy.py
usage: backupboy.py [-h] --server SERVER --user Username --software Name
                    --subject Subject [--port 143] [--index CSV Index]
                    [--folder INBOX] [--since 01-Apr-2018] [--sender Name]
                    [--jobname DailyJob] [--force] [--ssl] [--tls]
                    [--password Password]
backupboy.py: error: the following arguments are required: --server, --user, --software, --subject
```

### 3.2 Help menu
Example of execution requesting help menu.

```sh
wesley@pyhost:~$ ./backupboy.py -h
usage: backupboy.py [-h] --server SERVER --user Username --software Name
                    --subject Subject [--port 143] [--index CSV Index]
                    [--folder INBOX] [--since 01-Apr-2018] [--sender Name]
                    [--jobname DailyJob] [--force] [--ssl] [--tls]
                    [--password Password]

Backupboy a backup log interpreter.

required arguments:
  --server SERVER      Imap server. "imap.mailserver.com"
  --user Username      Imap user
  --software Name      Software target {backupexec_en-us, backupexec_pt-br,
                       cobian_en-us, cobian_pt-br, robocopy_en-us,
                       robocopy_pt-br}
  --subject Subject    Mail subject text. "Some other subject"

optional arguments:
  --port 143           Imap server port. Default=143
  --index CSV Index    The first csv collumn
  --folder INBOX       The imap target folder "INBOX/Backup XYZ".
                       Default="INBOX"
  --since 01-Apr-2018  Mails since date
  --sender Name        Mail sender name. "The BackupBoy"
  --jobname DailyJob   Custom job name. Combined with --software robocopy_[*]
  --force              Ignore invalid logs.
  --ssl                Use ssl encrypted connection.
  --tls                Use tls encrypted connection.
  --password Password  Imap password.
```

### 3.2 Cobian log processing

> Requirements
> - One mail for each job.
> - Log compressed in ZIP format.

Running example: Processing a backup log of Cobian software.

```sh
wesley@pythost:~$ ./backupboy.py --server imap.server.com --user user.name --software cobian_en-us --subject Backup --port 993 --ssl --password mypassword
Backup Pictures;2018-01-30 14:43;2018-01-30 14:43;0;5,57 MB
Backup Pictures;2018-01-30 15:25;2018-01-30 15:25;0;5,57 MB
```

### 3.3 Backup Exec log processing

> Requirements
> - Attached log.

Running example: Processing a backup log of Backup Exec software.

```sh
wesley@pyhost:~$ ./backupboy.py --server imap.server.com --port 993 --user user.name --software backupexec_en-us --folder "INBOX/Backup Boy" --subject "Backup Exec" --since 29-Jan-2018 --sender "Backup Boy" --ssl --password mypassword
Daily-Full;wednesday, 24 of january of 2018 at 23:00:04;thursday, 25 de january de 2018 at 02:25:23;Failed
Daily-Full;thursday, 25 of january of 2018 at 23:00:04;friday, 26 of january of 2018 at 04:24:19;Successful
Daily-Full;friday, 26 of january of 2018 at 23:00:02;saturday, 27 of january of 2018 at 02:18:27;Failed
```

### 3.4 Robocopy log processing

> Requirements
> - One mail for each job.
> - Log compressed in ZIP format.

Running example: Processing a backup log of Robocopy software

```sh
wesley@pyhost:~$ ./backupboy.py --server imap.server.com --port 993 --user user.name --software robocopy_en-us --folder "INBOX/Backup Boy" --subject "Robocopy: Daily Job" --since 29-Jan-2018 --jobname "Segunda" --ssl --password mypassword
Daily;Mon Jan 29 20:00:01 2018;Tue Jan 30 00:14:54 2018;0
```

### 4. Future features
- Standardization of start and end job times
- Code optimization and redundancy elimination
- Multiple processing request with json on stdin

### 5. License
MIT
