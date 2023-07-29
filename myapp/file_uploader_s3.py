from concurrent.futures import ThreadPoolExecutor
import os
import boto3
from botocore.exceptions import NoCredentialsError, BotoCoreError
from boto3.s3.transfer import S3UploadFailedError


class FileUploader:
    def __init__(self, aws_access_key_id, aws_secret_access_key, bucket_name):
        self.s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name='sa-east-1')  # include your region here
        self.bucket_name = bucket_name

    def upload_file(self, file_name, folder_path):
        try:
            print(f"Uploading {file_name}...")
            self.s3.upload_file(os.path.join(
                folder_path, file_name), self.bucket_name, file_name)
            print(f"{file_name} uploaded successfully")
        except NoCredentialsError:
            print("Credentials not available")
        except BotoCoreError as e:
            print(f"BotoCoreError: {e}")
        except S3UploadFailedError as e:
            print(f"S3UploadFailedError: {e}")

    def upload_files(self, folder_path):
        print("Starting upload...")
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(self.upload_file, os.listdir(folder_path), [
                         folder_path]*len(os.listdir(folder_path)))

        print("Upload completed. Deleting local files...")
        # Delete local files
        for file_name in os.listdir(folder_path):
            os.remove(os.path.join(folder_path, file_name))
        print("Local files deleted.")
