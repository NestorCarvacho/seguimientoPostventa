from django.contrib import admin
from .models import PostVenta, TipoPostVenta, Comite

# Register your models here.
admin.site.register(TipoPostVenta)

@admin.register(PostVenta)
class PostVentaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_remitente', 'tipo_postventa_display', 'estado', 'fecha_envio_correo')
    list_filter = ('estado', 'fecha_envio_correo')
    search_fields = ('nombre_remitente', 'direccion_vivienda', 'numero_contacto')

    def tipo_postventa_display(self, obj):
        return ", ".join([tipo.nombre for tipo in obj.tipo_postventa.all()])
    tipo_postventa_display.short_description = 'Tipo de Postventa'

@admin.register(Comite)
class ComiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)
