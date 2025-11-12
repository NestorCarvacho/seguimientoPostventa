from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import Http404
from .models import PostVenta, Comite, TipoUsuario
from .forms import PostVentaForm, UserUpdateForm, UserCreateForm, UserPasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

# Vista de prueba para dropdown
def test_dropdown(request):
    """Vista simple para probar Bootstrap dropdown"""
    return render(request, 'test_dropdown.html')

def test_datatables_simple(request):
    """Vista simple para probar DataTables"""
    from django.http import HttpResponse
    with open('test_datatables.html', 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html')

def test_datatables_independent(request):
    """Test independiente de DataTables con datos reales"""
    from .models import PostVenta
    postventas = PostVenta.objects.all()[:20]  # Solo primeros 20 registros
    return render(request, 'test_datatables_independent.html', {'postventas': postventas})

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class PermissionMixin(UserPassesTestMixin):
    """Mixin para verificar permisos basados en tipo de usuario"""
    required_permission = None
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
            
        # Superusuarios y staff tienen todos los permisos
        if user.is_superuser or user.is_staff:
            return True
            
        # Verificar si el usuario tiene tipo_usuario asignado
        if not hasattr(user, 'tipo_usuario') or not user.tipo_usuario:
            return False
            
        tipo_usuario = user.tipo_usuario
        
        # Mapeo de permisos
        permission_map = {
            'puede_crear_postventa': tipo_usuario.puede_crear_postventa,
            'puede_ver_todas_postventas': tipo_usuario.puede_ver_todas_postventas,
            'puede_editar_todas_postventas': tipo_usuario.puede_editar_todas_postventas,
            'puede_eliminar_todas_postventas': tipo_usuario.puede_eliminar_todas_postventas,
            'puede_editar_propias_postventas': tipo_usuario.puede_editar_propias_postventas,
            'puede_eliminar_propias_postventas': tipo_usuario.puede_eliminar_propias_postventas,
            'puede_gestionar_usuarios': tipo_usuario.puede_gestionar_usuarios,
            'puede_gestionar_comites': tipo_usuario.puede_gestionar_comites,
        }
        
        return permission_map.get(self.required_permission, False)
        
    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permisos para realizar esta acción.')
        return redirect('postventa:list')

@method_decorator(login_required, name='dispatch')
class PostVentaListView(ListView):
    model = PostVenta
    template_name = 'postventa/postventa_list.html'
    context_object_name = 'postventas'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostVentaForm()
        
        # Pasar permisos al template
        user = self.request.user
        context['user_permissions'] = {
            'puede_crear': self._user_can_create(),
            'puede_ver_todas': self._user_can_view_all(),
            'puede_editar_todas': self._user_can_edit_all(),
            'puede_eliminar_todas': self._user_can_delete_all(),
            'puede_editar_propias': self._user_can_edit_own(),
            'puede_eliminar_propias': self._user_can_delete_own(),
        }
        return context

    def get_queryset(self):
        user = self.request.user
        if self._user_can_view_all():
            return PostVenta.objects.all().select_related('usuario', 'usuario__comite')
        return PostVenta.objects.filter(usuario=user).select_related('usuario', 'usuario__comite')
    
    def _user_can_view_all(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_ver_todas_postventas
        return False
    
    def _user_can_create(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_crear_postventa
        return True  # Por defecto pueden crear
    
    def _user_can_edit_all(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_editar_todas_postventas
        return False
    
    def _user_can_delete_all(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_eliminar_todas_postventas
        return False
    
    def _user_can_edit_own(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_editar_propias_postventas
        return True  # Por defecto pueden editar las propias
    
    def _user_can_delete_own(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            return user.tipo_usuario.puede_eliminar_propias_postventas
        return True  # Por defecto pueden eliminar las propias

@method_decorator(login_required, name='dispatch')
class PostVentaCreateView(SuccessMessageMixin, CreateView):
    model = PostVenta
    form_class = PostVentaForm
    template_name = 'postventa/postventa_form.html'
    success_url = reverse_lazy('postventa:list')
    success_message = 'Solicitud de postventa creada exitosamente.'

    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario puede crear post-ventas
        user = request.user
        if user.is_superuser or user.is_staff:
            return super().dispatch(request, *args, **kwargs)
            
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario:
            if not user.tipo_usuario.puede_crear_postventa:
                messages.error(request, 'No tienes permisos para crear post-ventas.')
                return redirect('postventa:list')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        response = super().form_valid(form)
        self.object.tipo_postventa.set(form.cleaned_data['tipo_postventa'])
        return response

@method_decorator(login_required, name='dispatch')
class PostVentaUpdateView(SuccessMessageMixin, UpdateView):
    model = PostVenta
    form_class = PostVentaForm
    template_name = 'postventa/postventa_form.html'
    success_url = reverse_lazy('postventa:list')
    success_message = 'Solicitud de postventa actualizada exitosamente.'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        
        # Verificar permisos
        if user.is_superuser or user.is_staff:
            return obj
            
        # Verificar si puede editar todas las post-ventas
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario and user.tipo_usuario.puede_editar_todas_postventas:
            return obj
            
        # Verificar si puede editar sus propias post-ventas
        if obj.usuario == user:
            if not hasattr(user, 'tipo_usuario') or not user.tipo_usuario:
                return obj  # Por defecto puede editar las propias
            if user.tipo_usuario.puede_editar_propias_postventas:
                return obj
                
        raise Http404("No tienes permisos para editar esta post-venta.")

@method_decorator(login_required, name='dispatch')
class PostVentaDeleteView(SuccessMessageMixin, DeleteView):
    model = PostVenta
    template_name = 'postventa/postventa_confirm_delete.html'
    success_url = reverse_lazy('postventa:list')
    success_message = 'Solicitud de postventa eliminada exitosamente.'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        
        # Verificar permisos
        if user.is_superuser or user.is_staff:
            return obj
            
        # Verificar si puede eliminar todas las post-ventas
        if hasattr(user, 'tipo_usuario') and user.tipo_usuario and user.tipo_usuario.puede_eliminar_todas_postventas:
            return obj
            
        # Verificar si puede eliminar sus propias post-ventas
        if obj.usuario == user:
            if not hasattr(user, 'tipo_usuario') or not user.tipo_usuario:
                return obj  # Por defecto puede eliminar las propias
            if user.tipo_usuario.puede_eliminar_propias_postventas:
                return obj
                
        raise Http404("No tienes permisos para eliminar esta post-venta.")

@method_decorator(login_required, name='dispatch')
class UserListView(PermissionMixin, ListView):
    model = User
    template_name = 'postventa/user_list.html'
    context_object_name = 'users'
    required_permission = 'puede_gestionar_usuarios'

    def get_queryset(self):
        return User.objects.all().select_related('comite', 'tipo_usuario').order_by('username')

@method_decorator(login_required, name='dispatch')
class UserCreateView(PermissionMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'postventa/user_form.html'
    success_url = reverse_lazy('postventa:user_list')
    success_message = 'Usuario creado exitosamente.'
    required_permission = 'puede_gestionar_usuarios'

@method_decorator(login_required, name='dispatch')
class UserUpdateView(PermissionMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'postventa/user_form.html'
    success_url = reverse_lazy('postventa:user_list')
    success_message = 'Usuario actualizado exitosamente.'
    required_permission = 'puede_gestionar_usuarios'

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])

@login_required
def user_change_password(request, pk):
    user = request.user
    # Verificar permisos
    if not (user.is_staff or user.is_superuser):
        if not (hasattr(user, 'tipo_usuario') and user.tipo_usuario and user.tipo_usuario.puede_gestionar_usuarios):
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('postventa:list')
    
    user_to_change = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password1']
            user_to_change.set_password(new_password)
            user_to_change.save()
            messages.success(request, f'Contraseña cambiada exitosamente para {user_to_change.username}.')
            return redirect('postventa:user_list')
    else:
        form = UserPasswordResetForm()
    
    return render(request, 'postventa/user_password_form.html', {
        'form': form,
        'user_to_change': user_to_change
    })

@method_decorator(login_required, name='dispatch')
class ComiteListView(PermissionMixin, ListView):
    model = Comite
    template_name = 'postventa/comite_list.html'
    context_object_name = 'comites'
    required_permission = 'puede_gestionar_comites'

@method_decorator(login_required, name='dispatch')
class ComiteCreateView(PermissionMixin, CreateView):
    model = Comite
    fields = ['nombre']
    template_name = 'postventa/comite_form.html'
    success_url = reverse_lazy('postventa:comite_list')
    required_permission = 'puede_gestionar_comites'

@method_decorator(login_required, name='dispatch')
class ComiteUpdateView(PermissionMixin, UpdateView):
    model = Comite
    fields = ['nombre']
    template_name = 'postventa/comite_form.html'
    success_url = reverse_lazy('postventa:comite_list')
    required_permission = 'puede_gestionar_comites'

@method_decorator(login_required, name='dispatch')
class ComiteDeleteView(PermissionMixin, DeleteView):
    model = Comite
    template_name = 'postventa/comite_confirm_delete.html'
    success_url = reverse_lazy('postventa:comite_list')
    required_permission = 'puede_gestionar_comites'

# Vistas para TipoUsuario
@method_decorator(login_required, name='dispatch')
class TipoUsuarioListView(AdminRequiredMixin, ListView):
    model = TipoUsuario
    template_name = 'postventa/tipo_usuario_list.html'
    context_object_name = 'tipos_usuario'

@method_decorator(login_required, name='dispatch')
class TipoUsuarioCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = TipoUsuario
    fields = [
        'nombre', 'nivel_acceso', 'descripcion', 'activo',
        'puede_crear_postventa', 'puede_ver_todas_postventas',
        'puede_editar_todas_postventas', 'puede_eliminar_todas_postventas',
        'puede_editar_propias_postventas', 'puede_eliminar_propias_postventas',
        'puede_gestionar_usuarios', 'puede_gestionar_comites'
    ]
    template_name = 'postventa/tipo_usuario_form.html'
    success_url = reverse_lazy('postventa:tipo_usuario_list')
    success_message = 'Tipo de usuario creado exitosamente.'

@method_decorator(login_required, name='dispatch')
class TipoUsuarioUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoUsuario
    fields = [
        'nombre', 'nivel_acceso', 'descripcion', 'activo',
        'puede_crear_postventa', 'puede_ver_todas_postventas',
        'puede_editar_todas_postventas', 'puede_eliminar_todas_postventas',
        'puede_editar_propias_postventas', 'puede_eliminar_propias_postventas',
        'puede_gestionar_usuarios', 'puede_gestionar_comites'
    ]
    template_name = 'postventa/tipo_usuario_form.html'
    success_url = reverse_lazy('postventa:tipo_usuario_list')
    success_message = 'Tipo de usuario actualizado exitosamente.'

@method_decorator(login_required, name='dispatch')
class TipoUsuarioDeleteView(AdminRequiredMixin, SuccessMessageMixin, DeleteView):
    model = TipoUsuario
    template_name = 'postventa/tipo_usuario_confirm_delete.html'
    success_url = reverse_lazy('postventa:tipo_usuario_list')
    success_message = 'Tipo de usuario eliminado exitosamente.'