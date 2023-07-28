from concurrent.futures import ThreadPoolExecutor
import os
import dropbox
from datetime import datetime


class FileUploader:
    def __init__(self, local_folder_path, dropbox_folder_path):
        self.dbx = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))
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
        current_month_index = datetime.now().month - 1
        return months_in_pt_br[current_month_index]

    def upload_file(self, file_name):
        local_file_path = os.path.join(self.local_folder_path, file_name)
        with open(local_file_path, 'rb') as local_file:
            file_content = local_file.read()
            dropbox_file_path = f"{self.dropbox_folder_path}/{self.folder_name}/{file_name}"
            self.dbx.files_upload(file_content, dropbox_file_path)
        # Delete local file
        os.remove(local_file_path)

    def upload_files(self):
        self.folder_name = self.get_current_month_name()
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.upload_file, os.listdir(self.local_folder_path))
