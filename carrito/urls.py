from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/aumentar/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('carrito/disminuir/<int:item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('pago/', views.pago_simulado, name='pago_simulado'),
    path('pago/exito/', views.pago_exitoso, name='pago_exitoso'),
    path('enviar_recibo/', views.recibir_correo, name='enviar_recibo'),

]