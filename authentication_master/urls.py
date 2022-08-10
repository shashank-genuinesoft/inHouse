from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
               
                path('admin/', admin.site.urls),
                path('api-auth/', include('rest_framework.urls')),
                path('', include("company.urls")),
                re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
                re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
              ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
