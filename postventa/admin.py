from django.contrib import admin
from .models import PostVenta, TipoPostVenta, Comite, TipoUsuario

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

@admin.register(TipoUsuario)
class TipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_acceso', 'activo', 'fecha_creacion')
    list_filter = ('nivel_acceso', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'nivel_acceso', 'descripcion', 'activo')
        }),
        ('Permisos de Post-ventas', {
            'fields': (
                'puede_crear_postventa',
                'puede_ver_todas_postventas', 
                'puede_editar_todas_postventas',
                'puede_eliminar_todas_postventas',
                'puede_editar_propias_postventas',
                'puede_eliminar_propias_postventas'
            )
        }),
        ('Permisos Administrativos', {
            'fields': ('puede_gestionar_usuarios', 'puede_gestionar_comites')
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        })
    )
