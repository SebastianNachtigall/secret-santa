#! /usr/bin/python

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class HtmlMail(object):
    """This class sends HTML emails"""

    def __init__(self, subject, sender, to, username, password,
            smtp="smtp.gmail.com", port=587):
        # Server attr
        self.server = smtplib.SMTP(smtp, port)
        self.username = username
        self.password = password
        # Mail attr
        self.subject = subject
        self.sender = sender
        self.to = to

    def send(self, message):
        """Send the html mail"""

        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.sender
        msg['To'] = self.to

        msg.attach(MIMEText(message, 'html'))

        self.server.starttls()
        self.server.login(self.username, self.password)
        self.server.sendmail(self.sender, self.to, msg.as_string())
        self.server.quit()
