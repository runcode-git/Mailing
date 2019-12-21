# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog
from lxml import html, etree

from mailing import HTML_FILE, MESSAGE_HTML, EDITOR_HTML
from py.static import create_message, open_file, read_file, save_file, parse_message


class LoadUpdateMassage:
    """ message loading and updating class """

    def __init__(self, parent):

        self.parent = parent
        self.message = ""

        create_message()
        self.load_message()

    def include_template(self):
        """ Include template message"""

        template = open_file(self.parent, HTML_FILE)

        if template:
            msg = "<div id='message'>" + (read_file(template)) + "</div>"
            save_file(MESSAGE_HTML, msg)

        self.load_message()

    def save_template(self):
        """save message template html """

        self.scan_message()
        save_dialog = QFileDialog.getSaveFileName(self.parent, 'Save File', './', 'HTML Files(*.html)')[0]
        if save_dialog != '':
            save_file(str(save_dialog), self.message)

    def scan_message(self):
        """ viewing the html message and then save message.html """

        self.parent.view_message.page().toHtml(self.save_message)

    def save_message(self, view_html):
        """ save message.html """

        tree = html.fromstring(view_html)
        element = tree.xpath("//div[@id='message_html']/child::*")[0]
        self.message = etree.tostring(element, encoding='unicode')  # encoding='unicode'
        save_file(MESSAGE_HTML, self.message)

    def load_message(self):
        """load and update message html """

        div = "//div[@id='message_html']"
        remove = "//div[@id='message']"
        message_div = parse_message(div, remove)

        message_html = read_file(MESSAGE_HTML)
        message_html = etree.HTML(message_html)
        message_div[0].append(message_html)

        html_edit = etree.tostring(message_div[1], method='html', encoding='unicode')
        save_file(EDITOR_HTML, html_edit)

        self.parent.view_message.load(QtCore.QUrl().fromLocalFile(f'/{EDITOR_HTML}'))
