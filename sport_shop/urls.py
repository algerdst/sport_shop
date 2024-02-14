from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from catalog.views import ProductViewSet

from . import settings
from rest_framework import routers

router=routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
print(router.urls)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls)),
    path('users/', include('users.urls')),
    path('', include('catalog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
