import boto3
from botocore.exceptions import NoCredentialsError
from botocore.exceptions import BotoCoreError, ClientError
from concurrent.futures import ThreadPoolExecutor
import os
from datetime import datetime


class FileUploader:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name='sa-east-1'
        )
        self.s3 = session.client('s3')
        self.bucket_name = bucket_name

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

    def get_unique_folder_name(self, base_name):
        i = 0
        while True:
            folder_name = f'{base_name}{i}' if i else base_name
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name, Prefix=folder_name)
            if 'Contents' not in response:
                return folder_name
            i += 1

    def upload_file(self, file_name, folder_path):
        try:
            print(f"Uploading {file_name}...")
            base_folder_name = self.get_current_month_name()
            folder_name = self.get_unique_folder_name(base_folder_name)
            self.s3.upload_file(os.path.join(folder_path, file_name),
                                self.bucket_name, f'{folder_name}/{file_name}')
            print(f"{file_name} uploaded successfully")
            os.remove(os.path.join(folder_path, file_name))
            print(f"Local file {file_name} deleted.")
        except NoCredentialsError:
            print("Credentials not available")
        except (BotoCoreError, ClientError) as error:
            print(f"Error uploading {file_name}. Error: {error}")

    def upload_files(self, folder_path):
        print("Starting upload...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.upload_file, os.listdir(folder_path), [
                         folder_path]*len(os.listdir(folder_path)))
        print("Upload completed.")
