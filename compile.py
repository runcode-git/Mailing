# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import os
import re
import secrets
import shutil
import sys
import traceback

import PyInstaller.__main__

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog, QListView, QTreeView, QFileSystemModel, QAbstractItemView, QApplication
from git import Repo, NoSuchPathError


class CreateInfo:

    def __init__(self):

        self.info = QSettings(f'.\\config\\info.ini', QSettings.IniFormat)
        self.info.setIniCodec('utf-8')

        self.user = os.getlogin()
        self.project = os.getcwd().split('\\')[-1]
        self.version = self.load_version()
        self.description = f'{self.project} - {self.create_description()}'
        self.copyright = f"www.{self.user.lower()}.ru"

        self.save_info()

    def save_info(self):

        info = self.generate_info()

        for item in info:
            self.info.beginGroup('Info')
            self.info.setValue(item, info[item])
            self.info.endGroup()

        print(':' * 100)
        print(f'{os.getcwd()}\\config\\info.ini file created successfully')

    def load_version(self):

        try:
            self.version = re.sub(r'^\s+|\n|\r|\s+$', '', Repo('.git').commit().message)

        except NoSuchPathError:

            self.version = input('Enter format version project 0.0.0.0\nversion:')

        return self.version

    def create_description(self):

        self.description = input('Enter description project \ndescription:')

        return self.description

    def generate_info(self):

        info = {
            'username': self.user,
            'name': self.project,
            'version': self.version,
            'description': self.description,
            'copyright': self.copyright
        }

        return info


class CompileProject:

    def __init__(self):

        self.install = []
        self.name = os.getcwd().split('\\')[-1]
        self.path = 'compile'
        self.key = secrets.token_hex(16)
        self.data = ""

        self.info = QSettings(f'./config/info.ini', QSettings.IniFormat)
        self.version = self.info.value('Info/version')

        self.create_path()
        self.create_info()

        self.compile()

    def compile(self):
        print(f'1. Compile project {self.name} ver.{self.version}')

        shutil.rmtree(os.path.join(f'{self.path}\\dist\\{self.name}'), ignore_errors=True)
        print('2. Start  PyInstaller...')
        PyInstaller.__main__.run(self.collect_install())

    def create_path(self):

        os.makedirs(self.path, exist_ok=True)

    @staticmethod
    def add_folders(app):

        dialog = QFileDialog()
        dialog.setOption(dialog.DontUseNativeDialog, True)
        dialog.setFileMode(dialog.DirectoryOnly)
        dialog.setDirectory(os.getcwd())

        for view in dialog.findChildren((QListView, QTreeView)):
            if isinstance(view.model(), QFileSystemModel):
                view.setSelectionMode(QAbstractItemView.MultiSelection)

        if dialog.exec_() == dialog.Accepted:
            return [directory.rsplit('/')[-1] for directory in dialog.selectedFiles()]

    def collect_install(self):

        self.project_name()
        self.dist_path()
        self.work_path()
        self.spec_path()
        # self.coding_key()

        if input('3. Add console? (y/n):') == 'n':
            self.wind_owed()
        else:
            self.no_wind_owed()

        if input('4. To collect in one exe file? (y/n):') == 'y':
            self.one_file()

        if input('5. Add resource folder? (y/n):') == 'y':
            self.data = self.add_folders(QApplication(sys.argv))
            self.add_data()

        self.version_file()
        self.icon()
        self.main_project()

        return self.install

    def project_name(self):

        self.install.append('--name=%s' % self.name.lower())

    def dist_path(self):

        self.install.append('--distpath=%s' % os.path.join(self.path, 'dist'))

    def one_file(self):

        self.install.append('--onefile')

    def wind_owed(self):

        self.install.append('--windowed')

    def no_wind_owed(self):

        self.install.append('--nowindowed')

    def coding_key(self):
        print(self.key)
        self.install.append('--key=%s' % self.key)

    def work_path(self):

        self.install.append('--workpath=%s' % os.path.join(self.path, 'build'))

    def spec_path(self):

        self.install.append('--specpath=%s' % os.path.join(self.path))

    def add_data(self):

        if self.data is not None:
            for item in self.data:
                self.install.append('--add-data=%s' % os.path.join(os.getcwd(), item, f';{item}'))

    def version_file(self):

        self.install.append('--version-file=%s' % os.path.join(f'info.{self.name.lower()}'))

    def icon(self):

        icon = f'{os.getcwd()}\\{self.name.lower()}.ico'
        if os.path.isfile(icon):
            self.install.append('--add-data=%s' % os.path.join(os.getcwd(), f'{self.name.lower()}.ico;.'))
            self.install.append('--icon=%s' % os.path.join(os.getcwd(), f'{self.name.lower()}.ico'))

    def main_project(self):

        self.install.append(os.path.join(os.getcwd(), f'{self.name.lower()}.py'))

    def create_info(self):

        info_content = self.generate_info()

        with open(f"{self.path}/info.{self.name.lower()}", 'w', encoding='utf-8') as file:
            file.write(info_content)
            file.close()

    def generate_info(self):

        ver_index = self.version.split('.')

        info_content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({ver_index[0]}, {ver_index[1]}, {ver_index[2]}, {ver_index[3]}),
    prodvers=({ver_index[0]}, {ver_index[1]}, {ver_index[2]}, {ver_index[3]}),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'{self.info.value('Info/username')}'),
        StringStruct(u'FileDescription', u'{self.info.value('Info/description')}'),
        StringStruct(u'FileVersion', u'{self.version}'),
        StringStruct(u'InternalName', u'cmd'),
        StringStruct(u'LegalCopyright', u'{self.info.value('Info/copyright')}'),
        StringStruct(u'OriginalFilename', u'{self.name}.exe'),
        StringStruct(u'ProductName', u'{self.name}'),
        StringStruct(u'ProductVersion', u'{self.version}')])]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
        return info_content

    # -------------------------------- end create


def setup_compile():
    print('Enter command number:\nversion(1)\ncompile(2)\nexit(3)\n')
    try:
        command = int(input('number:'))

        if command == 1:
            try:
                CreateInfo()

            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())

        elif command == 2:

            if not f'{os.getcwd()}\\config\\info.ini':
                CreateInfo()

            CompileProject()

        elif command >= 3:
            exit()

    except ValueError:
        print('Not a number but a string!')


if __name__ == '__main__':
    setup_compile()
