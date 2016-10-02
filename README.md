Ansible Role: Dovecot
=====================

[Dovecot](http://www.dovecot.org/) is an open source IMAP and POP3 email server for Linux/UNIX-like systems, written with security primarily in mind.

This role is part of the [Mailserver](https://github.com/mailserver) project.

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
