"""
Vistas de la aplicación de inventario.
Maneja la lógica de negocio para autenticación, gestión de insumos y movimientos.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Insumo, Movimiento
from .forms import InsumoForm, MovimientoForm


# ==================== AUTENTICACIÓN ====================

def register(request):
    """
    Vista para el registro de nuevos usuarios.
    
    Permite a usuarios nuevos crear una cuenta en el sistema.
    Después del registro exitoso, el usuario es autenticado automáticamente
    y redirigido a la lista de insumos.
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        
    Returns:
        HttpResponse: Renderiza el formulario de registro o redirige a insumos
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Guardar el nuevo usuario
            user = form.save()
            # Autenticar automáticamente al usuario recién registrado
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente! Bienvenido al sistema.')
            return redirect('insumo_list')
    else:
        # Mostrar formulario vacío para GET request
        form = UserCreationForm()
    
    return render(request, 'inventario/register.html', {'form': form})


# ==================== VISTAS DE INSUMOS ====================

class InsumoListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los insumos del inventario.
    
    Muestra una tabla con todos los insumos registrados en el sistema,
    incluyendo código, nombre, stock actual y ubicación.
    Requiere que el usuario esté autenticado.
    
    Attributes:
        model: Modelo Insumo a listar
        template_name: Template HTML a renderizar
        context_object_name: Nombre de la variable en el template
    """
    model = Insumo
    template_name = 'inventario/insumo_list.html'
    context_object_name = 'insumos'
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto del template"""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Insumos'
        return context


class InsumoCreateView(LoginRequiredMixin, CreateView):
    """
    Vista para crear un nuevo insumo.
    
    Permite agregar un nuevo insumo al inventario con todos sus datos:
    código, nombre, descripción, stock inicial y ubicación.
    
    Attributes:
        model: Modelo Insumo a crear
        form_class: Formulario a utilizar
        template_name: Template HTML a renderizar
        success_url: URL a la que redirigir después de crear exitosamente
    """
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/insumo_form.html'
    success_url = reverse_lazy('insumo_list')
    
    def form_valid(self, form):
        """Ejecuta acciones adicionales cuando el formulario es válido"""
        messages.success(self.request, 'Insumo creado exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto del template"""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nuevo Insumo'
        context['boton_texto'] = 'Crear Insumo'
        return context


class InsumoUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar un insumo existente.
    
    Permite modificar los datos de un insumo ya registrado en el sistema.
    
    Attributes:
        model: Modelo Insumo a editar
        form_class: Formulario a utilizar
        template_name: Template HTML a renderizar
        success_url: URL a la que redirigir después de editar exitosamente
    """
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/insumo_form.html'
    success_url = reverse_lazy('insumo_list')
    
    def form_valid(self, form):
        """Ejecuta acciones adicionales cuando el formulario es válido"""
        messages.success(self.request, 'Insumo actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto del template"""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['boton_texto'] = 'Guardar Cambios'
        return context


class InsumoDeleteView(LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar un insumo.
    
    Solicita confirmación antes de eliminar un insumo del sistema.
    NOTA: Si el insumo tiene movimientos asociados, también se eliminarán
    debido a la configuración CASCADE en el modelo.
    
    Attributes:
        model: Modelo Insumo a eliminar
        template_name: Template HTML de confirmación
        success_url: URL a la que redirigir después de eliminar exitosamente
    """
    model = Insumo
    template_name = 'inventario/insumo_confirm_delete.html'
    success_url = reverse_lazy('insumo_list')
    
    def delete(self, request, *args, **kwargs):
        """Ejecuta acciones adicionales al eliminar"""
        messages.success(self.request, 'Insumo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ==================== VISTAS DE MOVIMIENTOS ====================

class MovimientoListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todos los movimientos de stock.
    
    Muestra un historial de todos los movimientos (entradas y salidas)
    registrados en el sistema, ordenados por fecha descendente
    (los más recientes primero).
    
    Attributes:
        model: Modelo Movimiento a listar
        template_name: Template HTML a renderizar
        context_object_name: Nombre de la variable en el template
        ordering: Orden de los registros (por fecha descendente)
    """
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']  # Más recientes primero
    
    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto del template"""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Historial de Movimientos'
        return context


@login_required
def movimiento_create(request):
    """
    Vista para crear un nuevo movimiento de stock.
    
    Permite registrar una entrada o salida de stock para un insumo.
    Actualiza automáticamente el stock_actual del insumo según el tipo
    de movimiento:
    - ENTRADA: suma la cantidad al stock actual
    - SALIDA: resta la cantidad del stock actual
    
    La vista también valida que haya stock suficiente antes de permitir
    una salida (validación realizada en el formulario).
    
    Args:
        request: Objeto HttpRequest con los datos de la petición
        
    Returns:
        HttpResponse: Renderiza el formulario o redirige a la lista de movimientos
    """
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            # Crear el movimiento sin guardarlo aún en la BD
            movimiento = form.save(commit=False)
            # Asignar el usuario actual al movimiento
            movimiento.usuario = request.user
            
            # Obtener el insumo relacionado
            insumo = movimiento.insumo
            
            # Actualizar el stock según el tipo de movimiento
            if movimiento.tipo == 'ENTRADA':
                # Entrada: aumentar el stock
                insumo.stock_actual += movimiento.cantidad
                mensaje = f'Entrada registrada: +{movimiento.cantidad} unidades de {insumo.nombre}'
            elif movimiento.tipo == 'SALIDA':
                # Salida: disminuir el stock
                insumo.stock_actual -= movimiento.cantidad
                mensaje = f'Salida registrada: -{movimiento.cantidad} unidades de {insumo.nombre}'
            
            # Guardar el insumo con el stock actualizado
            insumo.save()
            # Guardar el movimiento en la base de datos
            movimiento.save()
            
            # Mostrar mensaje de éxito
            messages.success(request, mensaje)
            return redirect('movimiento_list')
    else:
        # Mostrar formulario vacío para GET request
        form = MovimientoForm()
    
    return render(request, 'inventario/movimiento_form.html', {
        'form': form,
        'titulo': 'Nuevo Movimiento',
        'boton_texto': 'Registrar Movimiento'
    })
