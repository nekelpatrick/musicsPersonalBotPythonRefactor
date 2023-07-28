from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import ItemViewSet
from .views import DownloadView




router = SimpleRouter()
router.register('items', ItemViewSet, basename='items')

urlpatterns = router.urls

urlpatterns = [
    path('download/', DownloadView.as_view(), name='download'),
]

