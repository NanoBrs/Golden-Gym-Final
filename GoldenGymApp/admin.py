from django.contrib import admin
from .models import Novedad

class NovedadAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_publicacion', 'imagen', 'ruta_video')  # Usa 'fecha_publicacion' y 'imagen'
    search_fields = ('titulo',)
    list_filter = ('fecha_publicacion',)  # Usa 'fecha_publicacion'

admin.site.register(Novedad, NovedadAdmin)
