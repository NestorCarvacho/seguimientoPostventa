from django import forms
from django.contrib.auth.models import User
from .models import PostVenta, TipoPostVenta

class PostVentaForm(forms.ModelForm):
    class Meta:
        model = PostVenta
        fields = [
            'nombre_remitente',
            'direccion_vivienda',
            'numero_contacto',
            'tipo_postventa',
            'estado',
            'fecha_envio_correo',
            'observaciones',
            'comentarios',
            'fecha_cierre',
            'numero_seguimiento',
        ]
        widgets = {
            'nombre_remitente': forms.TextInput(attrs={'class': 'form-control neumorphic-input'}),
            'direccion_vivienda': forms.TextInput(attrs={'class': 'form-control neumorphic-input'}),
            'numero_contacto': forms.TextInput(attrs={'class': 'form-control neumorphic-input'}),
            'tipo_postventa': forms.CheckboxSelectMultiple(attrs={'class': 'neumorphic-checkbox'}),
            'estado': forms.Select(attrs={'class': 'form-select neumorphic-input'}),
            'fecha_envio_correo': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control neumorphic-input'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control neumorphic-input'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control neumorphic-input'}),
            'fecha_cierre': forms.DateInput(attrs={'type': 'date', 'class': 'form-control neumorphic-input', 'disabled': 'true'}),
            'numero_seguimiento': forms.TextInput(attrs={'class': 'form-control neumorphic-input', 'placeholder': 'Número entregado por la empresa'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'fecha_envio_correo' in self.changed_data:
            instance.fecha_envio_correo = self.cleaned_data['fecha_envio_correo']
        if commit:
            instance.save()
        return instance

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'comite']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comite': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_staff:
            self.fields['comite'].disabled = True