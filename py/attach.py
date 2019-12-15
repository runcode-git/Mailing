# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import os

from PyQt5.QtWidgets import QDialog, QFileDialog
from lxml import etree

from Mailing import EDITOR_HTML
from py.static import parse_message, save_file


class FileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setFileMode(QFileDialog.ExistingFiles)

    def accept(self):
        super(FileDialog, self).accept()


class AttachClearFile:
    """ the class attaches files and deletes """

    def __init__(self, parent):
        self.parent = parent
        self.array_files = []

    def add_file(self):
        """ Attach file open ui """

        dialog = FileDialog(self.parent)
        if dialog.exec_() == QDialog.Accepted:

            for item in dialog.selectedFiles():
                self.array_files.append(item)

        self.attach_file_message()
        return self.array_files

    def attach_file_message(self):
        """add message file dvi html """

        div = "//file"
        remove = "//file/div"
        message_file = parse_message(div, remove)

        for item_file in self.array_files:
            file_name = os.path.basename(item_file)  # вытаскивай имя и раширение фала
            file_size = os.stat(item_file).st_size  # вытаскивай размер в байтах
            file_size = float(("%.1f" % (file_size / 1024)))

            file_div = f"""
            <div class="alert alert-secondary w-auto float-left m-2 small">
                <i class="fas fa-paperclip mr-2"></i>
                <span class="font-weight-bold">{file_name}</span> ({file_size}kb)
            </div>
            """

            message_file[0].append(etree.HTML(file_div))

        html_edit = etree.tostring(message_file[1], method='html', encoding='unicode')
        save_file(EDITOR_HTML, html_edit)

    def clear_attach_file(self):
        """ Clear file attach"""
        self.array_files.clear()
        self.attach_file_message()
