from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Insumo, Movimiento
from .forms import InsumoForm, MovimientoForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('insumo_list')
    else:
        form = UserCreationForm()
    return render(request, 'inventario/register.html', {'form': form})

# Vistas para Insumo
class InsumoListView(LoginRequiredMixin, ListView):
    model = Insumo
    template_name = 'inventario/insumo_list.html'
    context_object_name = 'insumos'

class InsumoCreateView(LoginRequiredMixin, CreateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/insumo_form.html'
    success_url = reverse_lazy('insumo_list')

class InsumoUpdateView(LoginRequiredMixin, UpdateView):
    model = Insumo
    form_class = InsumoForm
    template_name = 'inventario/insumo_form.html'
    success_url = reverse_lazy('insumo_list')

class InsumoDeleteView(LoginRequiredMixin, DeleteView):
    model = Insumo
    template_name = 'inventario/insumo_confirm_delete.html'
    success_url = reverse_lazy('insumo_list')

# Vistas para Movimiento
class MovimientoListView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'inventario/movimiento_list.html'
    context_object_name = 'movimientos'
    ordering = ['-fecha']

@login_required
def movimiento_create(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            
            # Actualizar stock del insumo
            insumo = movimiento.insumo
            if movimiento.tipo == 'ENTRADA':
                insumo.stock_actual += movimiento.cantidad
            elif movimiento.tipo == 'SALIDA':
                insumo.stock_actual -= movimiento.cantidad
            
            insumo.save()
            movimiento.save()
            return redirect('movimiento_list')
    else:
        form = MovimientoForm()
    return render(request, 'inventario/movimiento_form.html', {'form': form})
