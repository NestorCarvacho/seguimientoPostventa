from django.urls import path
from .views import (
    PostVentaListView,
    PostVentaCreateView,
    PostVentaUpdateView,
    PostVentaDeleteView,
    UserListView,
    UserUpdateView,
    ComiteListView,
    ComiteCreateView,
    ComiteUpdateView,
    ComiteDeleteView
)

app_name = 'postventa'

urlpatterns = [
    path('', PostVentaListView.as_view(), name='list'),
    path('crear/', PostVentaCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', PostVentaUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', PostVentaDeleteView.as_view(), name='delete'),
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/editar/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('comites/', ComiteListView.as_view(), name='comite_list'),
    path('comites/crear/', ComiteCreateView.as_view(), name='comite_create'),
    path('comites/editar/<int:pk>/', ComiteUpdateView.as_view(), name='comite_update'),
    path('comites/eliminar/<int:pk>/', ComiteDeleteView.as_view(), name='comite_delete'),
]