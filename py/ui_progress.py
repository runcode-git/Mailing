# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import random
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt

from py.send import SendMessage
from py.static import connect_ui, close_dialog


class SendMessageThread(QThread):
    """class Thread Mailing send_messages"""
    send_signal = pyqtSignal()

    def __init__(self, malling):
        super().__init__()

        self.malling = malling

    def run(self):
        self.malling.send_messages()
        self.send_signal.emit()


class UiStartMailing(QtWidgets.QDialog):
    """class Progress Send messages"""

    signal_start_timer = pyqtSignal()
    signal_stop_timer = pyqtSignal()
    signal_count_process = pyqtSignal()
    signal_send_end = pyqtSignal()
    signal_send_start = pyqtSignal()

    def __init__(self, data, parent=None):
        super(UiStartMailing, self).__init__(parent)

        connect_ui(self, 'ui/progress.ui')
        self.parent = parent

        self.clc_message = SendMessage(data)
        self.timer = QTimer()

        self.count_email = self.clc_message.count_email
        self.count_email_bar = self.count_email
        self.emails = self.clc_message.emails

        self.message = None
        self.server = None
        self.thread = None
        self.done = True

        self.line = "*" * 100

        self.init_send_ui()

    def init_send_ui(self):
        """ init ui """

        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
        # ----------------------------
        self.progress_message.setStyleSheet("QProgressBar {font: 8pt 'Verdana'}")
        self.progress_message.setFormat(f"-- {self.count_email} emails sent --")
        self.progress_message.setMaximum(int(self.count_email))
        self.progress_message.setValue(0)

        self.progress_email.setStyleSheet("QProgressBar {font: 8pt 'Verdana'}")
        self.progress_email.setFormat(f"-- 0 message --")
        self.progress_email.setValue(0)

        # ----------------------------
        self.timer.timeout.connect(self.process_message_email)
        self.signal_start_timer.connect(lambda: self.timer.start(200))
        self.signal_stop_timer.connect(self.timer.stop)
        self.signal_count_process.connect(lambda: self.process_send_email(self.count_email))
        self.signal_send_end.connect(lambda: self.progress_email.setValue(100))
        self.signal_send_start.connect(lambda: self.progress_email.setValue(0))

        self.btn_start.clicked.connect(self.start_stop)

    def start_stop(self):
        """load file template html """

        if self.btn_start.isChecked():
            self.start_thread()

        else:
            self.done = False

    def start_thread(self):
        """ start thread send messages """

        self.thread = SendMessageThread(self)
        self.thread.send_signal.connect(self.stop_sent)
        self.thread.start()

    def send_messages(self):
        """ global def send messages """

        for send in range(len(self.emails)):

            sends = self.emails[send]
            self.clc_message.server_start()  # start server

            for item in range(len(sends)):

                if self.done:
                    self.send_out(sends[item])
                else:
                    break

            self.clc_message.server_stop()
            self.progress_email.setFormat(f"-- send {self.count_email_bar} message --")

        self.progress_message.setFormat("All letters to addresses have been sent successfully!")

    def send_out(self, name_email):
        """ send out"""

        name = name_email[0]
        email = name_email[1]

        self.progress_email.setFormat(f"-- {name} : {email} --")

        if self.timer.isActive() is False:
            self.signal_start_timer.emit()
        self.signal_count_process.emit()

        self.clc_message.create_message(name)
        self.clc_message.send(email)
        self.update_progress_bar()

    def update_progress_bar(self):
        """ finish update send """

        time_send = random.uniform(0.1, 2)

        self.signal_stop_timer.emit()  # stop timer
        self.signal_send_end.emit()  # progress bar 100%
        time.sleep(1)
        self.signal_send_start.emit()  # progress bar 0%

        if self.count_email != 0:
            update = "loading"
            num = 5
            for i in range(num):
                time.sleep(time_send)
                self.progress_email.setFormat(f"{'-' * i} {update} {'-' * i}")

            time.sleep(time_send)

    def stop_sent(self):
        """ process message progress bar"""

        print(self.line, '\n', "Сервер оставнолен!")

        self.signal_stop_timer.emit()
        self.btn_start.setChecked(False)
        self.btn_start.setCheckable(True)
        self.progress_email.setValue(0)
        self.progress_message.setValue(0)
        self.thread = None
        close_dialog(self)

    def process_message_email(self):
        """ process message progress bar"""

        value = self.progress_email.value() + 1
        self.progress_email.setValue(value)

    def process_send_email(self, count):
        """ count send progress bar"""

        self.count_email = int(count) - 1
        self.progress_message.setFormat(f"-- left to send: {str(self.count_email)} --")
        current_value = self.progress_message.value() + 1
        self.progress_message.setValue(current_value)