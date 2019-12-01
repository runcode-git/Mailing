# -*- coding: utf-8 -*-
#  ---------------------------------------------------------------------------------------------------------------------
import csv
import os

from PyQt5.QtGui import QIcon

from main import CSV_FILE, GROUP_EMAIL, PROJECT, resource_path
from py.static import open_file


class DataBaseCsv:
    """ class for adding csv file with email base """

    def __init__(self, parent):

        self.parent = parent
        self.count_email = 0
        self.list_email = None

        self.include_csv()

    def include_csv(self):
        """ we include the csv file email """

        file_csv = open_file(self.parent, CSV_FILE)

        if file_csv:
            self.count_email_base(file_csv)
            self.update_csv_status(file_csv)

            self.list_email = self.split_email_csv(self.array_group_csv(file_csv), GROUP_EMAIL)

    def update_csv_status(self, file_csv):
        """ update menu csv status """

        if int(self.count_email) > 0:
            self.parent.download_data.setIcon(QIcon(resource_path('icons/recipient.png')))
            self.parent.setWindowTitle(
                f"{PROJECT} | {self.parent.from_email} | {os.path.basename(file_csv)}")

    def count_email_base(self, file_csv):
        """ we read the email addresses in the csv file """

        with open(file_csv, encoding='utf-8') as file:
            self.count_email = str(sum(1 for line in file) - 1)

    @staticmethod
    def array_group_csv(file_csv):
        """ array group csv file """

        group_csv = []
        with open(file_csv, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for names, emails in reader:
                group_csv.append([names, emails])
        return group_csv

    @staticmethod
    def split_email_csv(arr, size):
        """ split email csv """

        array = []
        while len(arr) > size:
            group = arr[:size]
            array.append(group)
            arr = arr[size:]
        array.append(arr)
        return array
