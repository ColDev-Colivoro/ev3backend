from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', views.register, name='register'),

    # Insumos
    path('', views.InsumoListView.as_view(), name='insumo_list'),
    path('insumo/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    path('insumo/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    path('insumo/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),

    # Movimientos
    path('movimientos/', views.MovimientoListView.as_view(), name='movimiento_list'),
    path('movimiento/nuevo/', views.movimiento_create, name='movimiento_create'),
]
