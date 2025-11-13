from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PostVenta, TipoPostVenta, Comite, TipoUsuario

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
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'comite', 'tipo_usuario']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comite': forms.Select(attrs={'class': 'form-select'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'is_staff': 'Es staff/administrador',
            'is_active': 'Usuario activo',
            'comite': 'Comité',
            'tipo_usuario': 'Tipo de Usuario'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comite'].queryset = Comite.objects.all()
        self.fields['comite'].empty_label = "Seleccione un comité"
        self.fields['tipo_usuario'].queryset = TipoUsuario.objects.filter(activo=True)
        self.fields['tipo_usuario'].empty_label = "Seleccione un tipo de usuario"

class UserSelfUpdateForm(forms.ModelForm):
    """Formulario reducido para que el propio usuario edite solo sus datos básicos.
    Excluye campos administrativos y evita modificar comité o tipo_usuario."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico'
        }

    def save(self, commit=True):
        """Forzar que comité y tipo_usuario permanezcan sin cambios aunque se intenten inyectar en POST."""
        instance = super().save(commit=False)
        # Seguridad: preservar comité y tipo_usuario originales
        original = User.objects.get(pk=instance.pk)
        instance.comite = original.comite
        instance.tipo_usuario = original.tipo_usuario
        if commit:
            instance.save(update_fields=['first_name', 'last_name', 'email'])
        return instance

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    is_staff = forms.BooleanField(required=False)
    is_active = forms.BooleanField(initial=True, required=False)
    comite = forms.ModelChoiceField(queryset=Comite.objects.all(), required=False, empty_label="Seleccione un comité")
    tipo_usuario = forms.ModelChoiceField(queryset=TipoUsuario.objects.filter(activo=True), required=False, empty_label="Seleccione un tipo de usuario")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'comite', 'tipo_usuario')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comite': forms.Select(attrs={'class': 'form-select'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
            'is_staff': 'Es staff/administrador',
            'is_active': 'Usuario activo',
            'comite': 'Comité',
            'tipo_usuario': 'Tipo de Usuario'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases CSS a los campos de contraseña
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['comite'].widget.attrs.update({'class': 'form-select'})
        self.fields['tipo_usuario'].widget.attrs.update({'class': 'form-select'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_staff = self.cleaned_data['is_staff']
        user.is_active = self.cleaned_data['is_active']
        if commit:
            user.save()
            if self.cleaned_data['comite']:
                user.comite = self.cleaned_data['comite']
            if self.cleaned_data['tipo_usuario']:
                user.tipo_usuario = self.cleaned_data['tipo_usuario']
            user.save()
        return user

class UserPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        max_length=128
    )
    new_password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        max_length=128
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2