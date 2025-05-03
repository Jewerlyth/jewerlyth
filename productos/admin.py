from django.contrib import admin
from .models import Categoria, ProductoJewe

class CategoriaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class ProductoJeweAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(ProductoJewe, ProductoJeweAdmin)