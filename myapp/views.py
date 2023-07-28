import os
import coreschema
from rest_framework.views import APIView
from rest_framework.response import Response
from myapp.fileuploader import FileUploader
from .utils import PlainTextParser, extract_youtube_urls, download_from_youtube, rename_files, rename_files_in_directory
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .utils import PlainTextParser, extract_youtube_urls, download_from_youtube, rename_files_in_directory


load_dotenv()  # take environment variables from .env.


class DownloadView(APIView):
    parser_classes = [PlainTextParser]

    @swagger_auto_schema(
        operation_description="Download YouTube videos and upload to Dropbox",
        request_body=openapi.Schema(
            type=openapi.TYPE_STRING,
            description="Text containing YouTube URLs",
            example="[16/7 11:55] Rodolfo Nekel: https://youtu.be/OIzP4ho4Q_I [16/7 11:58] Rodolfo Nekel: https://youtu.be/5XzifsdU7AM [16/7 12:04] Rodolfo Nekel: https://youtu.be/Dra-ZOvkuuM [17/7 10:34] Rodolfo Nekel: https://youtu.be/LWQb7984Fy8 [17/7 10:43] Rodolfo Nekel: https://youtu.be/rCgLBUHbJr0 [17/7 10:46] Rodolfo Nekel: https://youtu.be/2rHSItnuZHo [17/7 10:47] Rodolfo Nekel: https://youtu.be/2GO6wdectr8 [17/7 10:49] Rodolfo Nekel: https://youtu.be/8ul6EljqoPM [17/7 10:55] Rodolfo Nekel: https://youtu.be/xIcAr7o3Neo [17/7 10:57] Rodolfo Nekel: https://youtu.be/SFhi2GKPxUk [17/7 11:01] Rodolfo Nekel: https://youtu.be/_2M3bSl3_ZI [17/7 11:06] Rodolfo Nekel: https://youtu.be/rBTwCWuvf-o [18/7 09:02] Rodolfo Nekel: https://youtu.be/jVZnBnwR7M0 [18/7 09:10] Rodolfo Nekel: https://youtu.be/qEDSk-N1wwU [18/7 13:17] Rodolfo Nekel: https://youtu.be/YhdqFhCSkPY [18/7 13:54] Rodolfo Nekel: https://youtu.be/2LwaDwreIFo [18/7 13:56] Rodolfo Nekel: https://youtu.be/TnD9eDgoaWM [18/7 13:56] Rodolfo Nekel: https://youtu.be/hB_H2RG66Tw [18/7 14:00] Rodolfo Nekel: https://youtu.be/u8eUUq-kFt4"
        ),
        responses={200: openapi.Response("success", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='The result of the operation'),
            },
            example={
                "status": "success"
            }
        ))}
    )
    def post(self, request, format=None):
        dropbox_token = os.getenv("DROPBOX_TOKEN")
        urls = extract_youtube_urls(request.data)
        download_from_youtube(urls)
        rename_files_in_directory('tmp')
        uploader = FileUploader('tmp', '/musicas-pai')
        uploader.upload_files()
        return Response({"status": "success"}, status=200)
