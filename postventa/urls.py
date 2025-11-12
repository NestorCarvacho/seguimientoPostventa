from django.urls import path
from .views import (
    PostVentaListView,
    PostVentaCreateView,
    PostVentaUpdateView,
    PostVentaDeleteView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    user_change_password,
    ComiteListView,
    ComiteCreateView,
    ComiteUpdateView,
    ComiteDeleteView,
    TipoUsuarioListView,
    TipoUsuarioCreateView,
    TipoUsuarioUpdateView,
    TipoUsuarioDeleteView,
    test_dropdown,
    test_datatables_simple,
    test_datatables_independent
)

app_name = 'postventa'

urlpatterns = [
    path('', PostVentaListView.as_view(), name='list'),
    path('crear/', PostVentaCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', PostVentaUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', PostVentaDeleteView.as_view(), name='delete'),
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/crear/', UserCreateView.as_view(), name='user_create'),
    path('usuarios/editar/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('usuarios/cambiar-password/<int:pk>/', user_change_password, name='user_change_password'),
    path('comites/', ComiteListView.as_view(), name='comite_list'),
    path('comites/crear/', ComiteCreateView.as_view(), name='comite_create'),
    path('comites/editar/<int:pk>/', ComiteUpdateView.as_view(), name='comite_update'),
    path('comites/eliminar/<int:pk>/', ComiteDeleteView.as_view(), name='comite_delete'),
    path('tipos-usuario/', TipoUsuarioListView.as_view(), name='tipo_usuario_list'),
    path('tipos-usuario/crear/', TipoUsuarioCreateView.as_view(), name='tipo_usuario_create'),
    path('tipos-usuario/editar/<int:pk>/', TipoUsuarioUpdateView.as_view(), name='tipo_usuario_update'),
    path('tipos-usuario/eliminar/<int:pk>/', TipoUsuarioDeleteView.as_view(), name='tipo_usuario_delete'),
    path('test-dropdown/', test_dropdown, name='test_dropdown'),
    path('test-datatables/', test_datatables_simple, name='test_datatables'),
    path('test-datatables-independent/', test_datatables_independent, name='test_datatables_independent'),
]