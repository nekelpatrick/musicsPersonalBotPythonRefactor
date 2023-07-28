import os
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.fileuploader import FileUploader
from .utils import PlainTextParser, extract_youtube_urls, download_from_youtube, rename_files, rename_files_in_directory
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


class DownloadView(APIView):
    parser_classes = [PlainTextParser]

    def post(self, request, format=None):
        dropbox_token = os.getenv('DROPBOX_TOKEN')
        urls = extract_youtube_urls(request.data)
        download_from_youtube(urls)
        rename_files_in_directory('tmp')
        uploader = FileUploader('tmp', '/musicas-pai', dropbox_token)
        uploader.upload_files()
        return Response({"status": "success"}, status=200)
