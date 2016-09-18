#!/usr/bin/env python

import sys
from subprocess import Popen
from email.parser import Parser
from email.utils import make_msgid
from subprocess import Popen, PIPE
from string import Template
import urllib2
import urllib
import smtplib

def mailFromTemplate(templatePath, user, percent):

        templateFile = open(templatePath, 'r')
        templateString = templateFile.read()
        template = Template(templateString)
        rendered = template.substitute(user=user, percent=percent)

        p = Parser()
        mail = p.parsestr(rendered)
        mail["Message-ID"] = make_msgid()

        return mail

errorRunningScript = False

try:
        percent = sys.argv[1]
        user    = sys.argv[2]
except IndexError as e:
        sys.stderr.write("Argument mismatch. Usage: [perecent exceeded] [user]\n")
        sys.exit(1)

# Make HTTP request
request_url = None
try:
    request_url_file = open('/etc/dovecot/dovecot-quota-warning-request-url', 'r')
    request_url = request_url_file.read()
except IOError as e:
    # File does not exist
    sys.stdout.write("Omitting HTTP POST request. Request URL file not found.\n")

if request_url != None:

    post_data = dict(user=user, percent=percent)

    try:
            u = urllib2.urlopen(request_url, data=urllib.urlencode(post_data))
    except Exception as e:
            sys.stderr.write("Could not make HTTP request: %s \n" % e)
            errorRunningScript = True

# User warning
user_warning = mailFromTemplate("/etc/dovecot/dovecot-quota-warning-template-user.txt", user, percent).as_string()

try:
        p = Popen(['/usr/lib/dovecot/dovecot-lda', "-d",user , '-o "plugin/quota=maildir:User quota:noenforcing"'], stdin=PIPE, stderr=PIPE, stdout=PIPE)
        (stdout, stderr) = p.communicate(user_warning)
        if p.returncode != 0:
                sys.stderr.write("Could not send user notification: %s\n" % stderr)
                errorRunningScript = True
except Exception as e:
        sys.stderr.write("Could not send user notification: %s\n" % e)
        errorRunningScript = True

# Admin warning
admin_warning = mailFromTemplate("/etc/dovecot/dovecot-quota-warning-template-admin.txt", user, percent)

try:
        server = smtplib.SMTP('localhost')
        server.sendmail(admin_warning["From"], [admin_warning["To"]], admin_warning.as_string())
        server.quit()
except Exception as e:
        sys.stderr.write("Could not send admin notification: %s\n" % e)
        errorRunningScript = True

# Return code

if errorRunningScript:
        sys.exit(1)
else:
        sys.exit(0)
