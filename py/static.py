# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import os
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
from main import ICON, MESSAGE_HTML, EDITOR_HTML
from lxml import html


def connect_ui(win, file_ui):
    """ load ui and icon"""

    try:
        uic.loadUi(file_ui, win)
        win.setWindowIcon(QIcon(ICON))

    except FileNotFoundError:
        uic.loadUi(resource_path(file_ui), win)
        win.setWindowIcon(QtGui.QIcon(resource_path(ICON)))


def open_file(dialog, file):
    """ open file dialog"""

    file = QFileDialog.getOpenFileName(dialog, "Open File", './', file)[0]

    if not os.path.exists(file):
        return

    return file


def domain_server(from_email):
    """ domain server """

    domain = from_email.rsplit('@', 2)
    return domain[1]


def read_file(name_file):
    """ reread html message """

    with open(name_file, 'r', encoding='utf-8') as file:
        file_read = file.read()
        file.close()
        return file_read


def save_file(name_file, message):
    """ create message.html """

    with open(name_file, 'w', encoding='utf-8') as file:
        file.write(message)
        file.close()


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


def create_message():
    """ create message.html """

    message = "<div id='message'><h1>Hello My Find</h1><p>message content</p></div>"
    save_file(MESSAGE_HTML, message)


def parse_message(div, remove=None):
    """ parse message"""

    editor = read_file(EDITOR_HTML)
    tree = html.fromstring(editor)

    div_edit = tree.xpath(div)[0]
    div_remove = tree.xpath(remove)

    for item in div_remove:
        item.getparent().remove(item)

    return div_edit, tree


def open_dialog(parent, dialog):
    """open dialog"""

    parent.setEnabled(False)
    dialog.setEnabled(True)

    if not dialog.exec_():
        parent.setEnabled(True)
        dialog.close()


def close_dialog(dialog):
    """close dialog"""

    dialog.close()
