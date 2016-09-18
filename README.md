Ansible Role: Dovecot
=====================

[Dovecot](http://www.dovecot.org/) is an open source IMAP and POP3 email server for Linux/UNIX-like systems, written with security primarily in mind.

This role is part of the [Mailserver](https://github.com/mailserver) project.

Examples
--------

### Dovecot IMAP with TLS and 2048 bit Diffie-Hellman parameter and MySQL backend

```yaml
- role: mailserver.dovecot
  hostname: "imap.example.com"
  dovecot_ssl_certificate: "/etc/letsencrypt/live/imap.example.com/fullchain.pem"
  dovecot_ssl_key: "/etc/letsencrypt/live/imap.example.com/privkey.pem"
  dh_parameters_length: 2048
  mysql:
    host: '127.0.0.1'
    user: 'dovecot'
    pass: 'correct horse battery staple'
    database: 'maildb'
```
