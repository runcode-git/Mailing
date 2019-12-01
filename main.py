# -*- coding: utf-8 -*-
#  www.runcode.ru
#  Project:Mailing |  Scripts:main.py | Author:RUNCODE | Date: 17.11.2019
#  --------------------------------------------------------------------------
import os
import sys
import time

from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen, QProgressBar


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def get_info(info):
    settings = QSettings('info.ini', QSettings.IniFormat)
    settings.setIniCodec('utf-8')

    return settings.value(f'Info/{info}')


NAME = get_info("name")
VERSION = get_info("version")
PROJECT = f"{NAME} {VERSION}"

ICON = f'{NAME}.ico'
MESSAGE_HTML = resource_path('editor/message.html')
EDITOR_HTML = resource_path('editor/editor.html')
CSV_FILE = 'CSV Files(*.csv)'
HTML_FILE = 'HTML Files(*.html)'
GROUP_EMAIL = 9  # колличество email в гуппе для расссылки

MSG_LOGIN_LINE = 'Your account name or password is incorrect'
MSG_ERROR_SERVER = 'The server responded weird stuff to my login request, please try again'
MSG_ERROR_LOGIN = 'Your account name or password is incorrect, please try again using the correct stuff'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    from py.ui_mailing import MallingApp

    mailing = MallingApp()

    splash_pix = QPixmap(resource_path('icons/splash_mailing.png'))
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setEnabled(False)

    progress_bar = QProgressBar(splash)
    progress_bar.setMaximum(10)
    progress_bar.setGeometry(25, splash_pix.height() - 50, splash_pix.width() - 50, 10)
    progress_bar.setTextVisible(False)

    progress_bar.setStyleSheet("QProgressBar {"
                               "background-color: #fff;"
                               "border-radius: 5px;"
                               "text-align: center; }"

                               "QProgressBar::chunk {"
                               "border-radius: 5px;"
                               "background-color: #4d5e6e; }")

    splash.show()
    splash.showMessage(f"<h4><font color='white'>{PROJECT}</h4>")

    for i in range(1, 11):
        progress_bar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    # Simulate something that takes time
    time.sleep(2)

    splash.finish(mailing)

    mailing.showMaximized()
    app.exec_()
