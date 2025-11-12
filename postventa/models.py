from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class TipoUsuario(models.Model):
    NIVEL_ACCESO_CHOICES = [
        ('revisor', 'Revisor - Solo lectura'),
        ('usuario', 'Usuario - Gestiona sus propias post-ventas'),
        ('supervisor', 'Supervisor - Ve todas, edita las propias'),
        ('administrador', 'Administrador - Control total'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    nivel_acceso = models.CharField(max_length=20, choices=NIVEL_ACCESO_CHOICES, default='usuario')
    descripcion = models.TextField(blank=True, null=True)
    
    # Permisos específicos
    puede_crear_postventa = models.BooleanField(default=True, help_text="Puede crear nuevas post-ventas")
    puede_ver_todas_postventas = models.BooleanField(default=False, help_text="Puede ver todas las post-ventas")
    puede_editar_todas_postventas = models.BooleanField(default=False, help_text="Puede editar todas las post-ventas")
    puede_eliminar_todas_postventas = models.BooleanField(default=False, help_text="Puede eliminar todas las post-ventas")
    puede_editar_propias_postventas = models.BooleanField(default=True, help_text="Puede editar sus propias post-ventas")
    puede_eliminar_propias_postventas = models.BooleanField(default=True, help_text="Puede eliminar sus propias post-ventas")
    
    # Permisos administrativos
    puede_gestionar_usuarios = models.BooleanField(default=False, help_text="Puede gestionar usuarios")
    puede_gestionar_comites = models.BooleanField(default=False, help_text="Puede gestionar comités")
    
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Usuario"
        verbose_name_plural = "Tipos de Usuario"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_acceso_display()})"

class PostVenta(models.Model):
    TIPO_POSTVENTA_CHOICES = [
        ('calefont', 'Calefont'),
        ('filtracion', 'Filtración de agua'),
        ('iluminaria', 'Iluminaria / Electricidad'),
        ('grietas', 'Grietas en muros o techos'),
        ('pintura', 'Pintura / Terminaciones'),
        ('puertas', 'Puertas o ventanas'),
        ('carpinteria', 'Carpintería / Muebles'),
        ('vidrios', 'Vidrios / Aluminio'),
        ('banio_cocina', 'Baños y cocina'),
    ]

    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_curso', 'En curso'),
        ('falta_material', 'Falta material'),
        ('cerrado', 'Cerrado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_remitente = models.CharField(max_length=255)
    direccion_vivienda = models.CharField(max_length=255)
    numero_contacto = models.CharField(max_length=15)
    tipo_postventa = models.ManyToManyField('TipoPostVenta')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    fecha_envio_correo = models.DateField(default=timezone.now)
    numero_seguimiento = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)
    fecha_cierre = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre_remitente} - {self.estado}"  

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es una nueva instancia
            self.fecha_envio_correo = self.fecha_envio_correo or timezone.now().date()
        else:  # Si es una instancia existente
            original = PostVenta.objects.get(pk=self.pk)
            self.fecha_envio_correo = original.fecha_envio_correo
        super().save(*args, **kwargs)

class TipoPostVenta(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Comite(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

User.add_to_class('comite', models.ForeignKey(Comite, on_delete=models.SET_NULL, null=True, blank=True, default=1))
User.add_to_class('tipo_usuario', models.ForeignKey(TipoUsuario, on_delete=models.SET_NULL, null=True, blank=True))
