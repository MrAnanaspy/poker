from .views import get_index
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

urlpatterns = [
    path('', get_index, name='get-data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)