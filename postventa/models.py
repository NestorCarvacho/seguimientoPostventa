from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

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
