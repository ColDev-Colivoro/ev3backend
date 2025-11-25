"""
Configuración de URLs para la aplicación de inventario.
Define las rutas para autenticación, gestión de insumos y movimientos.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ==================== AUTENTICACIÓN ====================
    # Ruta para el login de usuarios
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    
    # Ruta para el logout de usuarios (redirige al login)
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Ruta para el registro de nuevos usuarios
    path('registro/', views.register, name='register'),

    # ==================== GESTIÓN DE INSUMOS ====================
    # Listar todos los insumos (ruta principal)
    path('insumos/', views.InsumoListView.as_view(), name='insumo_list'),
    
    # Crear un nuevo insumo
    path('insumos/nuevo/', views.InsumoCreateView.as_view(), name='insumo_create'),
    
    # Editar un insumo existente
    path('insumos/<int:pk>/editar/', views.InsumoUpdateView.as_view(), name='insumo_update'),
    
    # Eliminar un insumo
    path('insumos/<int:pk>/eliminar/', views.InsumoDeleteView.as_view(), name='insumo_delete'),

    # ==================== GESTIÓN DE MOVIMIENTOS ====================
    # Listar todos los movimientos (entradas y salidas)
    path('movimientos/', views.MovimientoListView.as_view(), name='movimiento_list'),
    
    # Crear un nuevo movimiento (entrada o salida de stock)
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
]
