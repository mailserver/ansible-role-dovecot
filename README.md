Ansible Role: Dovecot
=====================

[Dovecot](http://www.dovecot.org/) is an open source IMAP and POP3 email server for Linux/UNIX-like systems, written with security primarily in mind.

This role is part of the [Mailserver](https://github.com/mailserver) project. Dovecot is used as virtual mail transport for Postfix and IMAP server.

Configuration
-------------

### dovecot_hostname

FQDN of the host running the mailserver. This domain is not allowed to be listed in the virtual domains. Defaults to the hostname from the Ansible facts, `ansible_fqdn`. 

### dovecot_default_mysql

The mysql credentials for the main mail database. This configuration option is ignored when the policy_source differs from `mysql`.

```yaml
dovecot_mysql:
  host: "127.0.0.1"
  port: 3306
  user: "dovecot"
  password:
  database: "mail"
```

### dovecot_config

Abstracts Dovecot specific configuration options.

#### listen

List of network addresses to listen to. Defaults to all IPv4 and IPv6 addresses available, `["*", "[::]"]`.

#### policy_source

Switches between different policy sources. At the moment `mysql` is the only supported source. Information about the used scheme can be found in the [mailserver.mysql-seed](https://github.com/mailserver/ansible-role-mysql-seed) repository.

#### vmail

| Key | Default | Description |
| --- | ------- | ----------- |
| user | `vmail` | Virtual owner of the mail directory |
| group | `vmail` | Virtual group of the mail directory |
| directory | `/var/mail` | Storage location of the mail directory |


#### auth

| Key | Default | Description |
| --- | ------- | ----------- |
| listen | `["inet", "unix"]` | Listen to network or local Unix sockets |
| inet | { address: '[::1]', port: 10026 } | Interface and listening port of the auth service" |
| unix | | Socket path and settings for Unix socket |

#### lmtp

| Key | Default | Description |
| --- | ------- | ----------- |
| listen | `["inet", "unix"]` | Listen to network or local Unix sockets |
| inet | "{ address: '[::1]', port: 10025 }" | Interface and listening port of the lmtp service" |
| unix | | Socket path and settings for Unix socket |

Read more: http://wiki.dovecot.org/LMTP

#### ssl

Encryption settings for SMTP. Used for client connections via StartTLS on the submission port (587) and Server-to-Server connections.

The default certificate and key paths point to Letsencryt. When not available, 2048 bit Diffie-Hellman parameters will be auto-generated.

| Key | Default | Description |
| --- | ------- | ----------- |
| key | `/etc/letsencrypt/live/{{ dovecot_hostname }}/privkey.pem` | Path to SSL key in PEM format |
| certificate | `/etc/letsencrypt/live/{{ dovecot_hostname }}/fullchain.pem` | Path to SSL certificate (chain) in PEM format |
| dhparams.length | 2048 | Size of Diffie-Hellman parameters |
| dhparams.file | `/etc/ssl/postfix_dhparams.pem` | Path to Diffie-Hellman parameters file |

#### managesieve_enabled

Enables Sieve and Managesieve with user based configuration. Is enabled by default.

#### config_dir

The folder in which the Dovecot configuration is stored. Defaults to `/etc/dovecot` on most operating systems.

Examples
--------

### Dovecot IMAP with TLS and 2048 bit Diffie-Hellman parameter and MySQL backend

```yaml
- role: mailserver.dovecot
  dovecot_hostname: "imap.example.com"
  dovecot_config:
    ssl:
      certificate: "/etc/letsencrypt/live/imap.example.com/fullchain.pem"
      key: "/etc/letsencrypt/live/imap.example.com/privkey.pem"
      dhparam:
        size: 2048
  dovecot_mysql:
    host: '127.0.0.1'
    user: 'dovecot'
    password: 'correct horse battery staple'
    database: 'maildb'
```
