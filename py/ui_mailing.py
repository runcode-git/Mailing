# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from main import PROJECT, QWebEngineSettings
from py.attach import AttachClearFile
from py.database import DataBaseCsv
from py.message import LoadUpdateMassage
from py.send import SendMessage
from py.static import *
from py.ui_login import LoginMail
from py.ui_progress import UiStartMailing


class MallingApp(QMainWindow):
    """class window Mailing"""

    def __init__(self):
        super().__init__()

        connect_ui(self, 'ui/window.ui')

        self.cls_attach = AttachClearFile(self)
        self.cls_message = LoadUpdateMassage(self)
        self.cls_login = LoginMail(self)

        self.from_email = None
        self.from_password = None
        self.data_emails = None
        self.data_files = []
        self.data = None

        self.ui_init()

    def ui_init(self):
        """ init ui """

        self.setWindowTitle(PROJECT)
        self.view_message.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, True)

        # -----------menu -------------------------

        self.login_from.triggered.connect(self.open_ui_login)
        self.download_data.triggered.connect(self.open_add_csv)
        self.attach_file.triggered.connect(self.open_attach_file)
        self.clear_file.triggered.connect(self.clear_attach_file)
        self.download_template.triggered.connect(self.open_template)
        self.save_message_template.triggered.connect(self.save_template)
        self.send_test.triggered.connect(self.send)
        self.start_send.triggered.connect(self.send)

        # -----------------------------------------

        self.cls_attach.attach_file_message()

        # ----------------temp---------------------
        # self.line_organisation.setText("Компания")
        # self.line_subject.setText("Тема сообщения")

    def set_data(self):
        """ set or update data"""

        self.data = {

            'from': self.from_email,
            'password': self.from_password,
            'organisation': self.line_organisation.text(),
            'subject': self.line_subject.text(),
            'files': self.data_files,
            'emails': self.data_emails
        }

    def open_ui_login(self):
        """ login open ui """

        open_dialog(self, self.cls_login)

        self.from_email = self.cls_login()[0]
        self.from_password = self.cls_login()[1]

        print(self.from_email, self.from_password)

    def open_add_csv(self):
        """ we include the csv file email """

        database = DataBaseCsv(self)
        self.data_emails = [database.list_email, database.count_email]
        print(self.data_emails)

    def open_attach_file(self):
        """ open file attachment dialog """

        self.cls_message.scan_message()
        self.data_files = self.cls_attach.add_file()
        self.cls_message.load_message()

    def clear_attach_file(self):
        """ Clear file attach"""

        self.cls_message.scan_message()
        self.cls_attach.clear_attach_file()
        self.cls_message.load_message()

    def open_template(self):
        """ open include template message"""

        self.cls_message.include_template()

    def save_template(self):
        """save message template html """

        self.cls_message.save_template()

    def send(self):
        """ send message """

        sender = self.sender()
        self.set_data()

        if sender.text() == 'send msg':  # send message testing

            if self.checking_data():

                load_send = SendMessage(self.data)
                load_send.create_message()
                load_send.send(self.from_email)
                load_send.server_stop()

                QMessageBox.information(self, 'Info', 'Test email sent to your email successfully! \n Check mail.')

        if sender.text() == 'sends msg':  # open sends

            if self.checking_data():

                self.cls_message.scan_message()
                ui_start = UiStartMailing(self.data, self)
                open_dialog(self, ui_start)

    def checking_data(self):
        """ checking data mailing"""

        for key in self.data.keys():

            if self.data[key] is None or self.data[key] == '':
                QMessageBox.warning(self, 'Info', f'There is {self.data[key]} data: {key}')
                break
        else:
            return True

    def closeEvent(self, event):
        """exit application """

        close = QMessageBox.question(self, "Quit", "Close the mailing application?", QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
