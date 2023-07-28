from rest_framework.views import APIView
from rest_framework.response import Response
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
from .utils import extract_urls


class DownloadView(APIView):
    def post(self, request, *args, **kwargs):
        urls = extract_urls(request.data)  # Extract URLs from user input
        files = self.download_songs(urls)
        self.convert_files(files)
        return Response({"message": "Download and conversion completed."})

    def download_songs(self, urls):
        download_options = {
            'format': 'bestaudio/best',
            'outtmpl': './tmp/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'nocheckcertificate': True,
        }
        with YoutubeDL(download_options) as ydl:
            ydl.download(urls)
        files = os.listdir('./tmp')
        return files

    def convert_files(self, files):
        for file in files:
            if file.endswith('.wav'):
                sound = AudioSegment.from_wav('./tmp/' + file)
                sound = sound.set_channels(2)
                sound = sound.set_frame_rate(44100)
                sound.export('./tmp/' + file, format="wav")
