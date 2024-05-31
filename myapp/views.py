import os
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.convert_to_wav import convert_to_wav
from myapp.file_uploader_s3 import FileUploader
from .utils import (
    PlainTextParser,
    extract_youtube_urls,
    download_from_youtube,
    rename_files_in_directory,
    delete_local_files,
)
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()  # Load environment variables from .env.


logger = logging.getLogger(__name__)


class DownloadView(APIView):
    parser_classes = [PlainTextParser]

    def post(self, request, format=None):
        logging.info("DownloadView POST request started")
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        local_folder_path = "tmp"

        try:
            # Extract URLs from the request data
            # Limit to 20 URLs
            urls = extract_youtube_urls(request.data)[:20]
            logging.info(f"Extracted URLs from user input: {urls}")

            # Synchronously execute operations in the defined order
            download_success = download_from_youtube(urls)
            if not download_success:
                logger.error("Download failed")
                return Response({"status": "error", "message": "Download failed"}, status=500)

            rename_files_in_directory(local_folder_path)
            convert_to_wav(local_folder_path)

            # Check the number of files in local_folder_path
            num_files = len(os.listdir(local_folder_path))
            if num_files > 20:
                return Response(
                    {"status": "error", "message": "More than 20 files to upload"},
                    status=400,
                )

            # Ensure only .wav files are uploaded
            wav_files = [f for f in os.listdir(local_folder_path) if f.endswith(".wav")]
            if not wav_files:
                return Response(
                    {"status": "error", "message": "No .wav files to upload"},
                    status=400,
                )

            uploader = FileUploader(aws_access_key_id, aws_secret_access_key, bucket_name)
            uploader.upload_files(local_folder_path)  # Assuming upload_files can accept a list of files to upload

            # Clean up
            delete_local_files(local_folder_path)

            return Response({"status": "success"}, status=200)
        except Exception as e:
            logging.error(f"Error in DownloadView POST request: {e}")
            traceback.print_exc()
            return Response({"status": "error", "message": str(e)}, status=500)
