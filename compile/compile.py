# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import datetime
import os
import re
import sys
import shutil

import PyInstaller.__main__
import PyInstaller.config

from PyQt5.QtCore import QSettings
from git import Repo

PATHPROJECT = (os.path.dirname(os.path.abspath('.')))
TODAY = datetime.date.today().year
USER = os.getlogin()
PROJECT = (re.findall(r'\w+$', PATHPROJECT))[0]  # project name
VERSION = re.sub(r'^\s+|\n|\r|\s+$', '', Repo('../.git').commit().message).split('.')  # version mailing 0.0.0.0
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
        StringStruct(u'ProductName', u'{PROJECT}'),
        StringStruct(u'ProductVersion', u'{VERSION[0]}.{VERSION[1]}')])]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
"""

COMMAND_BAT = f"""
pyinstaller -w -D -i {os.getcwd()}\\{PROJECT}.ico 
--version-file info.{PROJECT} 
--add-data "{os.getcwd()}\\ui\\*.ui;ui" 
--add-data "{os.getcwd()}\\py\\*.py;py" 
--add-data "{os.getcwd()}\\icons\\*.png;icons" 
--add-data "{os.getcwd()}\\editor;editor" 
--add-data "{os.getcwd()}\\info.ini;." 
--add-data "{os.getcwd()}\\{PROJECT}.ico;." 
-n {PROJECT} {os.getcwd()}\\main.py"""

INFO = {
    'username': USER,
    'name': PROJECT,
    'version': f'{VERSION[0]}.{VERSION[1]}.{VERSION[2]}',
    'description': DESCRIPTION,
    'copyright': COPYRIGHT
}

path = '..\\exe'
os.makedirs(path, exist_ok=True)

def create_info():
    with open(f"{path}/info.{PROJECT}", 'w', encoding='utf-8') as file:
        file.write(VERSION_INFO)
        file.close()


# def create_bat():
#     with open(f"{path}/{PROJECT}.bat", 'w', encoding='utf-8') as file:
#         file.write(re.sub(r'^\s+|\n|\r|\s+$', '', COMMAND_BAT))
#         file.close()

def compile_project():

    shutil.rmtree(os.path.join(f'.\\dist\\{PROJECT}'), ignore_errors=True)
    # удаляем папку скомпелированного проекта, если  она существует

    PyInstaller.__main__.run([
        '--name=%s' % PROJECT,
        # '--distpath=%s' % os.path.join(path, 'dist'),
        # '--workpath=%s' % os.path.join(path, 'buld'),
        # '--specpath=%s' % os.path.join(path),
        # '--onefile',
         '--windowed',
        # '--key='
        '--add-data=%s' % os.path.join('..', 'ui', '*.ui;ui'),
        '--add-data=%s' % os.path.join('..', 'py', '*.py;py'),
        '--add-data=%s' % os.path.join('..', 'icons', '*.png;icons'),
        '--add-data=%s' % os.path.join('..', 'editor', ';editor'),
        '--version-file=%s' % os.path.join('.', f'info.{PROJECT}'),
        '--icon=%s' % os.path.join('..', f'{PROJECT}.ico'),
        '--add-data=%s' % os.path.join('..', 'info.ini;.'),
        '--add-data=%s' % os.path.join('..', f'{PROJECT}.ico;.'),
        os.path.join('..', f'{PROJECT}.py'),
    ])


def version_project():
    settings = QSettings(f'..\\info.ini', QSettings.IniFormat)
    settings.setIniCodec('utf-8')

    for item in INFO:
        settings.beginGroup('Info')
        settings.setValue(item, INFO[item])
        settings.endGroup()


if __name__ == '__main__':
    version_project()
    # create_info()
    compile_project()
    # create_bat()
