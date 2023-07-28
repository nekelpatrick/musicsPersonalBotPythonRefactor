from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import PlainTextParser, extract_youtube_urls, download_from_youtube, rename_files, rename_files_in_directory

class DownloadView(APIView):
    parser_classes = [PlainTextParser]

    def post(self, request, format=None):
        urls = extract_youtube_urls(request.data)
        download_from_youtube(urls)
        rename_files_in_directory('tmp')
        return Response({"status": "success"}, status=200)
