from django.urls import path
from Jewerlythwebapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="Home"),
    path('carrito', views.carrito, name="Carrito"),
    path('soporte', views.soporte, name="Soporte"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)