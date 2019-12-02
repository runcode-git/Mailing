# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import smtplib
import ssl

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox

from main import MSG_LOGIN_LINE, MSG_ERROR_SERVER, MSG_ERROR_LOGIN, PROJECT, resource_path
from py.static import connect_ui, close_dialog, domain_server


class LoginMail(QtWidgets.QDialog):
    """class window Browsers messages"""

    def __init__(self, parent=None):
        super(LoginMail, self).__init__(parent)

        self.parent = parent
        self.from_email = None
        self.password = None

        self.settings = QSettings('login.ini', QSettings.IniFormat)
        self.settings.setIniCodec('utf-8')

        self.init_login_ui()

    def init_login_ui(self):
        """initialize login ui"""

        connect_ui(self, 'ui/login.ui')
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)

        self.btn_login.clicked.connect(self.login_sender_email)
        self.chk_save_login.stateChanged.connect(self.save_login)
        # ---------------------------------------------

        email_password = self.settings.value('Login/email')

        if email_password:
            self.line_from_email.setText(self.settings.value('Login/email'))
            self.line_from_password.setText(self.settings.value('Login/password'))

        # email = runcode@bk.ru
        # password = 3MEUR9preif^
        # ---------------------------------------------

    def save_login(self, state):
        """ save email and pssaword"""

        if state == Qt.Checked:

            self.settings.beginGroup('Login')
            self.settings.setValue("email", self.line_from_email.text())
            self.settings.setValue("password", self.line_from_password.text())
            self.settings.endGroup()

        else:
            self.settings.clear()

    def set_from(self):
        """ set from email """

        self.from_email = self.line_from_email.text()
        return self.from_email

    def set_password(self):
        """ set from password """

        self.password = self.line_from_password.text()
        return self.password

    def login_sender_email(self):
        """login to sender email"""

        if str(self.set_from()) != "" and str(self.set_password()) != "":

            if self.server_start():

                self.update_parent()
                close_dialog(self)

            else:
                self.btn_login.setCheckable(False)

        else:
            self.btn_login.setCheckable(False)
            QMessageBox.warning(self.parent, 'Error email and password', MSG_LOGIN_LINE)

    def server_start(self):
        """ server login start """
        try:
            domain = f"smtp.{domain_server(self.from_email)}"
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL(domain, 465, context=context) as server:

                server.login(self.from_email, self.password)
                server.quit()

                return True

        except smtplib.SMTPHeloError:

            QMessageBox.warning(self.parent, 'Error', MSG_ERROR_SERVER)
            return False

        except smtplib.SMTPAuthenticationError:

            QMessageBox.warning(self.parent, 'Error', MSG_ERROR_LOGIN)
            return False

    def update_parent(self):
        """ update mailing title and menu"""

        self.parent.setWindowTitle(f"{PROJECT} | {self.from_email}")
        self.parent.login_from.setIcon(QIcon(resource_path('icons/sender.png')))
        self.parent.login_from.setToolTip(f"login: {self.from_email}")

    def __call__(self):
        """the correct email and password"""

        return self.from_email, self.password
