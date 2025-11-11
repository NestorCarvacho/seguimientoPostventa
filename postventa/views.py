from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import PostVenta, Comite
from .forms import PostVentaForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

@method_decorator(login_required, name='dispatch')
class PostVentaListView(ListView):
    model = PostVenta
    template_name = 'postventa/postventa_list.html'
    context_object_name = 'postventas'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostVentaForm()
        return context

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return PostVenta.objects.all()
        return PostVenta.objects.filter(usuario=self.request.user)

@method_decorator(login_required, name='dispatch')
class PostVentaCreateView(SuccessMessageMixin, CreateView):
    model = PostVenta
    form_class = PostVentaForm
    template_name = 'postventa/postventa_form.html'
    success_url = reverse_lazy('postventa:list')
    success_message = 'Solicitud de postventa creada exitosamente.'

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

@method_decorator(login_required, name='dispatch')
class PostVentaDeleteView(SuccessMessageMixin, DeleteView):
    model = PostVenta
    template_name = 'postventa/postventa_confirm_delete.html'
    success_url = reverse_lazy('postventa:list')
    success_message = 'Solicitud de postventa eliminada exitosamente.'

@method_decorator(login_required, name='dispatch')
class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'postventa/user_list.html'
    context_object_name = 'users'

@method_decorator(login_required, name='dispatch')
class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'postventa/user_form.html'

    def get_success_url(self):
        return reverse_lazy('postventa:user_list')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.kwargs['pk'])

@method_decorator(login_required, name='dispatch')
class ComiteListView(AdminRequiredMixin, ListView):
    model = Comite
    template_name = 'postventa/comite_list.html'
    context_object_name = 'comites'

@method_decorator(login_required, name='dispatch')
class ComiteCreateView(AdminRequiredMixin, CreateView):
    model = Comite
    fields = ['nombre']
    template_name = 'postventa/comite_form.html'
    success_url = reverse_lazy('postventa:comite_list')

@method_decorator(login_required, name='dispatch')
class ComiteUpdateView(AdminRequiredMixin, UpdateView):
    model = Comite
    fields = ['nombre']
    template_name = 'postventa/comite_form.html'
    success_url = reverse_lazy('postventa:comite_list')

@method_decorator(login_required, name='dispatch')
class ComiteDeleteView(AdminRequiredMixin, DeleteView):
    model = Comite
    template_name = 'postventa/comite_confirm_delete.html'
    success_url = reverse_lazy('postventa:comite_list')