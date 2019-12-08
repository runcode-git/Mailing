# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import os

import PyInstaller.__main__
print(os.path.join('.', 'py', '*.py'))
PyInstaller.__main__.run([
    '--name=%s' % 'Mailing',
    '--onefile',
    # '--windowed',
    '--add-data=%s' % os.path.join('.', 'ui', '*.ui;ui'),
    '--add-data=%s' % os.path.join('.', 'py', '*.py;py'),
    '--add-data=%s' % os.path.join('.', 'icons', '*.png;icons'),
    '--add-data=%s' % os.path.join('.', 'editor', '*;editor'),
    '--version-file=%s' % os.path.join('.', '.', 'info.Mailing'),
    '--icon=%s' % os.path.join('.', '.', 'Mailing.ico'),
    os.path.join('.', 'main.py'),
])