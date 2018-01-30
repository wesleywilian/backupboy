# backupboy

> [Readme in English](README.md)


> [Readme in Portuguese](README_PT-BR.md)


### 1. Introdução
Softwares de backup são ótimas ferramentas em uma infraestrutura, não apenas no contexto corporativo, mas também no contexto individual.

Entretanto, no momento em que há centenas de softwares de backup assim como muitas rotinas, torna-se custoso o gerenciamento do resultado dessas rotinas de backup, prejudicando a identificação de problemas e o correto funcionamento dessas.

**Backupboy** é um projeto do qual tem o objetivo de solucionar o problema citado, através da interpretação dos logs de diversos softwares em diferentes idiomas.

### 2. Funcionamento
**Backupboy** é um projeto escrito em Python do qual baixa logs de backups via e-mail utilizando o protocolo IMAP, descompacta o arquivo caso seja necessário e captura informações relevantes para gerar uma saída objetiva do estado da rotina de backup.

#### 2.1 Softwares suportados
- Cobian Backup 11
- Backup Exec
- Robocopy

#### 2.2 Compatibilidade

Abaixo, a tabela descreve a atual compatibilidade do Backupboy.

|Software|Nome da rotina de backup|Horário de início da rotina|Horário do término da rotina|Estado da rotina|Volume de dados|
|-|-|-|-|-|-|
|Cobian Backup 11|Compatível|Compatível|Compatível|Captura o número de erros da rotina|Compatível|
|Backup Exec|Compatível|Compatível|Compatível|Captura o estado da rotina|-|
|Robocopy|Informado com o argumento --jobname|Compatível|Compatível|Captura o número de erros da rotina|-|

#### 2.3 Idiomas

Abaixo, os idiomas suportados no momento.

|Software|Idioma|
|-|-|
|Cobian Backup 11|Inglês|
|Cobian Backup 11|Português do Brasil|
|Backup Exec|Inglês|
|Backup Exec|Português do Brasil|
|Robocopy|Inglês|
|Robocopy|Português do Brasil|

#### 2.4 Saídas disponíveis
- CSV: Formato de saída do qual utiliza caracteres chave para delimitar o conteúdo dos dados

### 3. Uso
Para utilizar o backupboy é necessário possuir acesso e credenciais validas em um servidor IMAP, utilizar Python 3.5 em ambiente Linux.

### 3.1 Execução sem argumentos

Abaixo exemplo de execução sem argumentos informados.

```sh
wesley@pyhost:~/backupboy$ ./backupboy.py
usage: backupboy.py [-h] --server SERVER --user Username --software Name
                    --subject Subject [--port 143] [--index CSV Index]
                    [--folder INBOX] [--since 01-Apr-2018] [--sender Name]
                    [--jobname DailyJob] [--force] [--ssl] [--tls]
                    [--password Password]
backupboy.py: error: the following arguments are required: --server, --user, --software, --subject
```

### 3.2 Menu de ajuda

Exemplo de execução solicitando exibição do menu de ajuda.

```sh
wesley@pyhost:~/backupboy$ ./backupboy.py -h
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

### 3.2 Interpretando log do Cobian

> Requerimentos
> - Um email para cada rotina.
> - Log compactado no formato ZIP.

Exemplo de execução: Interpretar um log de backup do software Cobian no idioma Português do Brasil.

```sh
wesley@pythost:~/backupboy$ ./backupboy.py --server imap.gmail.com --user user.name --software cobian_pt-br --subject Backup --port 993 --ssl --password mypassword
Backup Fotos;2018-01-30 12:00;2018-01-30 12:01;0;155,57 MB
Backup Fotos;2018-01-29 12:00;2018-01-29 12:01;0;155,57 MB
Backup Fotos;2018-01-28 12:00;2018-01-28 12:01;0;155,62 MB
```

### 3.3 Interpretando log do Backup Exec

> Requerimentos
> - Log anexado ao email.

Exemplo de execução: Interpretar um log de backup do software Backup Exec no idioma Português do Brasil.

```sh
wesley@pyhost:~/backupboy$ ./backupboy.py --server imap.gmail.com --port 993 --user user.name --software backupexec_pt-br --folder "INBOX/Backup Boy" --subject "Alerta do Backup Exec" --since 29-Jan-2018 --sender "Backup Boy" --ssl --password mypassword
Diario;segunda-feira, 29 de janeiro de 2018 às 19:00:00;terça-feira, 30 de janeiro de 2018 às 01:05:25;concluído com exceções
```

### 3.4 Interpretando log do Robocopy

> Requerimentos
> - Um email para cada rotina.
> - Log compactado no formato ZIP.

Exemplo de execução: Interpretar um log de backup do software Robocopy no idioma Português do Brasil.

```sh
wesley@pyhost:~/backupboy$ ./backupboy.py --server imap.gmail.com --port 993 --user user.name --software robocopy_pt-br --folder "INBOX/Backup Boy" --subject "Robocopy: Backup Diario" --since 29-Jan-2018 --jobname "Segunda" --ssl --password mypassword
Segunda;Mon Jan 29 20:00:01 2018;Tue Jan 30 00:14:54 2018;0
```

### 4. Futuras funcionalidades
- Captura e padronização dos horários de início e fim da rotina
- Reestruturação de código, otimizar e eliminar redundâncias
- Múltiplas verificações através de requisição json via stdin

### 5. Licença
MIT
