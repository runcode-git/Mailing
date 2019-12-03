# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import smtplib
import ssl
import os
import traceback
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from lxml import etree, html

from main import MESSAGE_HTML
from py.static import domain_server, read_file, save_file


class SendMessage:
    """ message creation and sending class """

    def __init__(self, data=None):

        self.data = data

        self.from_email = data['from']
        self.password = data['password']
        self.files = data['files']
        self.emails = data['emails'][0]
        self.organisation = data['organisation']
        self.subject = data['subject']
        self.domain = f"smtp.{domain_server(self.from_email)}"
        self.count_email = data['emails'][1]

        self.message = None
        self.server = None

        self.server_start()

    def server_start(self):
        """ server login start """

        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(self.domain, 465, context=context)
        self.server.login(self.from_email, self.password)

    def create_message(self, recipient=None):
        """ create message """
        try:
            template_msg = read_file(MESSAGE_HTML)
            tree = html.fromstring(template_msg)
            recipient_names = tree.xpath("//recipient")
            for name in recipient_names:
                name.text = recipient

            html_edit = etree.tostring(tree, encoding='unicode')

            save_file(MESSAGE_HTML, html_edit)
            self.message = read_file(MESSAGE_HTML)

        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

    @staticmethod
    def file_message(files, msg_part):
        """ Open file in binary mode """

        with open(files, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(files)}",
        )
        msg_part.attach(part)

    def send(self, email):
        """ send message """
        try:
            msg = MIMEMultipart()
            msg.attach(MIMEText(self.message, "html"))

            for file in self.files:
                self.file_message(file, msg)

            msg.add_header('Content-Type', 'text/html')
            msg['Subject'] = self.subject
            msg["Date"] = formatdate(localtime=True)
            msg['From'] = formataddr((str(Header(self.organisation, 'utf-8')), self.from_email))

            self.server.sendmail(msg['From'], email, msg.as_string())

        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())

    def server_stop(self):
        """ server stop and quit """

        self.server.quit()
