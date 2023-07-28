import time
from dropbox import Dropbox, exceptions
import os
from datetime import datetime


class FileUploader:
    def __init__(self, local_folder_path, dropbox_folder_path, token):
        self.dbx = Dropbox(token)
        self.local_folder_path = local_folder_path
        self.dropbox_folder_path = dropbox_folder_path

    @staticmethod
    def get_current_month_name():
        months_in_pt_br = [
            "Janeiro",
            "Fevereiro",
            "Março",
            "Abril",
            "Maio",
            "Junho",
            "Julho",
            "Agosto",
            "Setembro",
            "Outubro",
            "Novembro",
            "Dezembro",
        ]
        current_month_index = time.localtime().tm_mon  # Month index is 1-based
        return months_in_pt_br[current_month_index - 1]

    def get_or_create_folder(self):
        month_name = self.get_current_month_name()
        folder_name = month_name
        counter = 1

        while True:
            try:
                self.dbx.files_get_metadata(os.path.join(
                    self.dropbox_folder_path, folder_name))
                folder_name = f"{month_name}{counter}"
                counter += 1
            except exceptions.ApiError as error:
                if error.error.is_path() and error.error.get_path().is_not_found():
                    self.dbx.files_create_folder_v2(os.path.join(
                        self.dropbox_folder_path, folder_name))
                    break
                raise error

        return folder_name

    def upload_files(self):
        files = os.listdir(self.local_folder_path)
        folder_name = self.get_or_create_folder()

        for file in files:
            file_path = os.path.join(self.local_folder_path, file)
            with open(file_path, "rb") as f:
                file_data = f.read()
            dropbox_path = os.path.join(
                self.dropbox_folder_path, folder_name, file)

            try:
                self.dbx.files_upload(file_data, dropbox_path)
            except exceptions.ApiError as error:
                print(f"Failed to upload {file} to Dropbox: {error}")
