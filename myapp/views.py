import os
import traceback
from .convert_to_wav import convert_to_wav
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.file_uploader_s3 import FileUploader
from .utils import (
    PlainTextParser,
    extract_youtube_urls,
    download_from_youtube,
    rename_files_in_directory,
    delete_local_files,
)
from dotenv import load_dotenv
from rest_framework.decorators import parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

load_dotenv()  # Load environment variables from .env.


class DownloadView(APIView):
    parser_classes = [PlainTextParser]

    def post(self, request, format=None):
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
        local_folder_path = "tmp"

        try:
            # Limit to 20 URLs
            urls = extract_youtube_urls(request.data)[:20]

            # Synchronously execute operations in the defined order
            download_from_youtube(urls)
            rename_files_in_directory(local_folder_path)
            convert_to_wav(local_folder_path)

            # Check the number of files in local_folder_path
            num_files = len(os.listdir(local_folder_path))
            if num_files > 20:
                return Response(
                    {"status": "error", "message": "More than 20 files to upload"},
                    status=400,
                )

            uploader = FileUploader(
                aws_access_key_id, aws_secret_access_key, bucket_name
            )
            uploader.upload_files(local_folder_path)

            # Clean up
            delete_local_files(local_folder_path)

            return Response({"status": "success"}, status=200)
        except Exception as e:
            traceback.print_exc()  # This will print the stack trace to the console
            return Response({"status": "error", "message": str(e)}, status=500)
