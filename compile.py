# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import datetime
import os
import re
import sys
import shutil

import PyInstaller.__main__
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QDialog, QFileDialog
from git import Repo

TODAY = datetime.date.today().year
USER = os.getlogin()
PROJECT = (re.findall(r'\w+$', os.getcwd()))[0]  # project name
project = PROJECT.lower()
VERSION = re.sub(r'^\s+|\n|\r|\s+$', '', Repo('.git').commit().message).split('.')  # version mailing 0.0.0.0
DESCRIPTION = f'{PROJECT} - Application for processing and sending emails to email.'
COPYRIGHT = f"{USER} © {TODAY}"

VERSION_INFO = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION[0]}, {VERSION[1]}, {VERSION[2]}, {VERSION[3]}),
    prodvers=({VERSION[0]}, {VERSION[1]}, {VERSION[2]}, {VERSION[3]}),
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
        [StringStruct(u'CompanyName', u'{USER}'),
        StringStruct(u'FileDescription', u'{DESCRIPTION}'),
        StringStruct(u'FileVersion', u'{VERSION[0]}.{VERSION[1]}'),
        StringStruct(u'InternalName', u'cmd'),
        StringStruct(u'LegalCopyright', u'{COPYRIGHT}'),
        StringStruct(u'OriginalFilename', u'{PROJECT}.exe'),
        StringStruct(u'ProductName', u'{project}'),
        StringStruct(u'ProductVersion', u'{VERSION[0]}.{VERSION[1]}')])]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

INFO = {
    'username': USER,
    'name': PROJECT,
    'version': f'{VERSION[0]}.{VERSION[1]}.{VERSION[2]}',
    'description': DESCRIPTION,
    'copyright': COPYRIGHT
}


def version_project():
    settings = QSettings(f'./config/info.ini', QSettings.IniFormat)
    settings.setIniCodec('utf-8')

    for item in INFO:
        settings.beginGroup('Info')
        settings.setValue(item, INFO[item])
        settings.endGroup()

    print('1. info.ini file created successfully')


class CompileProject:

    def __init__(self, name_path, name_project):
        self.install = []
        self.name = name_project
        self.path = name_path
        self.key = ""
        self.data = ['py', 'ui', 'editor', 'icons', 'config']

        self.create_path()
        self.create_info()

    def compile(self):
        print(f'2. Compile project {self.name} {VERSION[0]}.{VERSION[1]}.{VERSION[2]}')

        shutil.rmtree(os.path.join(f'{self.path}\\dist\\{self.name}'), ignore_errors=True)
        print('3. Start  PyInstaller...')
        PyInstaller.__main__.run(self.collect_install())

    def create_path(self):

        os.makedirs(self.path, exist_ok=True)

    def collect_install(self):

        self.project_name()
        self.dist_path()
        self.wind_owed()
        self.work_path()
        self.spec_path()
        self.add_data()
        self.version_file()
        self.icon()
        self.main_project()

        return self.install

    def create_info(self):

        with open(f"{self.path}/info.{self.name.lower()}", 'w', encoding='utf-8') as file:
            file.write(VERSION_INFO)
            file.close()

    def project_name(self):

        self.install.append('--name=%s' % self.name)

    def dist_path(self):

        self.install.append('--distpath=%s' % os.path.join(self.path, 'dist'))

    def one_file(self):

        self.install.append('--onefile')

    def wind_owed(self):

        self.install.append('--windowed')

    def coding_key(self):

        self.install.append('--key=%s' % self.key)

    def work_path(self):

        self.install.append('--workpath=%s' % os.path.join(self.path, 'build'))

    def spec_path(self):

        self.install.append('--specpath=%s' % os.path.join(self.path))

    def add_data(self):

        for item in self.data:
            self.install.append('--add-data=%s' % os.path.join(os.getcwd(), item, f';{item}'))

    def version_file(self):

        self.install.append('--version-file=%s' % os.path.join(f'info.{self.name.lower()}'))

    def icon(self):

        self.install.append('--add-data=%s' % os.path.join(os.getcwd(), f'{self.name.lower()}.ico;.'))
        self.install.append('--icon=%s' % os.path.join(os.getcwd(), f'{self.name.lower()}.ico'))

    def main_project(self):

        self.install.append(os.path.join(os.getcwd(), f'{self.name.lower()}.py'))

    # -------------------------------- end create


def setup_compile():

    print('Enter command number:\n1 - version]\n2 - compile\n3 - exit\n')

    command = input('number:')

    if int(command) == 1:

        version_project()

    elif int(command) == 2:

        version_project()
        run_compile = CompileProject('compile', PROJECT)
        run_compile.compile()

    elif int(command) >= 3:
        exit()


if __name__ == '__main__':

    setup_compile()
