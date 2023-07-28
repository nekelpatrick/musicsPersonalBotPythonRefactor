from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import yt_dlp


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class DownloadView(APIView):
    def post(self, request, *args, **kwargs):
        urls = request.data
        for url in urls:
            yt_dlp.YoutubeDL().download([url])
        return Response({"message": "Download completed."})
