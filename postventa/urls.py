from django.urls import path
from .views import (
    PostVentaListView,
    PostVentaCreateView,
    PostVentaUpdateView,
    PostVentaDeleteView,
    UserListView,
    UserUpdateView
)

app_name = 'postventa'

urlpatterns = [
    path('', PostVentaListView.as_view(), name='list'),
    path('crear/', PostVentaCreateView.as_view(), name='create'),
    path('editar/<int:pk>/', PostVentaUpdateView.as_view(), name='update'),
    path('eliminar/<int:pk>/', PostVentaDeleteView.as_view(), name='delete'),
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/editar/', UserUpdateView.as_view(), name='user_update'),
]