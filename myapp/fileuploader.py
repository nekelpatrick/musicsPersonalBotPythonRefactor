import os
import dropbox
from dropbox.exceptions import AuthError, ApiError
from concurrent.futures import ThreadPoolExecutor
import time

class FileUploader:
    def __init__(self, local_folder_path, dropbox_folder_path, dropbox_token):
        self.dbx = dropbox.Dropbox(dropbox_token)
        self.local_folder_path = local_folder_path
        self.dropbox_folder_path = dropbox_folder_path

    def upload_file(self, file_name):
        local_file_path = os.path.join(self.local_folder_path, file_name)
        dropbox_file_path = f"{self.dropbox_folder_path}/{file_name}"
        with open(local_file_path, "rb") as file:
            try:
                self.dbx.files_upload(file.read(), dropbox_file_path)
            except ApiError as e:
                if e.error.is_path() and \
                        e.error.get_path().is_conflict():
                    print(f"Conflict with file: {file_name}.")
                elif e.user_message_text:
                    print(e.user_message_text)
                else:
                    print(e)
            except AuthError as e:
                print(f"Authentication error: {e}")

    def upload_files(self, max_workers=5):
        files = os.listdir(self.local_folder_path)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(self.upload_file, files)
