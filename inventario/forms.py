"""
Formularios de la aplicación de inventario.
Define los formularios para la creación y edición de Insumos y Movimientos.
"""
from django import forms
from .models import Insumo, Movimiento


class InsumoForm(forms.ModelForm):
    """
    Formulario para crear y editar insumos.
    
    Incluye todos los campos necesarios para registrar un insumo:
    código, nombre, descripción, stock actual y ubicación.
    Todos los campos tienen estilos Bootstrap aplicados.
    """
    
    class Meta:
        model = Insumo
        fields = ['codigo', 'nombre', 'descripcion', 'stock_actual', 'ubicacion']
        
        # Widgets personalizados con clases de Bootstrap
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: HER-001'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Motosierra STIHL MS 381'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del insumo...'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Almacén Principal - Sección A1'
            }),
        }
        
        # Labels personalizados en español
        labels = {
            'codigo': 'Código del Insumo',
            'nombre': 'Nombre del Insumo',
            'descripcion': 'Descripción',
            'stock_actual': 'Stock Actual',
            'ubicacion': 'Ubicación en Almacén',
        }
        
        # Textos de ayuda para cada campo
        help_texts = {
            'codigo': 'Código único identificador (ej: HER-001, EPP-002)',
            'nombre': 'Nombre descriptivo del insumo',
            'descripcion': 'Descripción detallada (opcional)',
            'stock_actual': 'Cantidad inicial en inventario',
            'ubicacion': 'Ubicación física en el almacén',
        }


class MovimientoForm(forms.ModelForm):
    """
    Formulario para registrar movimientos de stock.
    
    Permite crear entradas o salidas de stock para un insumo específico.
    Incluye validación automática para evitar salidas cuando no hay
    stock suficiente.
    """
    
    class Meta:
        model = Movimiento
        fields = ['insumo', 'tipo', 'cantidad']
        
        # Widgets personalizados con clases de Bootstrap
        widgets = {
            'insumo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': '1'
            }),
        }
        
        # Labels personalizados en español
        labels = {
            'insumo': 'Insumo',
            'tipo': 'Tipo de Movimiento',
            'cantidad': 'Cantidad',
        }
        
        # Textos de ayuda para cada campo
        help_texts = {
            'insumo': 'Selecciona el insumo a mover',
            'tipo': 'Entrada (ingreso) o Salida (egreso) de stock',
            'cantidad': 'Cantidad de unidades a mover',
        }

    def clean(self):
        """
        Validación personalizada del formulario.
        
        Verifica que haya stock suficiente antes de permitir una salida.
        Si el tipo es SALIDA y no hay stock suficiente, genera un error.
        
        Returns:
            dict: Datos limpios y validados del formulario
            
        Raises:
            ValidationError: Si se intenta una salida sin stock suficiente
        """
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')
        insumo = cleaned_data.get('insumo')

        # Validar solo si es una SALIDA
        if tipo == 'SALIDA' and insumo and cantidad:
            # Verificar si hay stock suficiente
            if insumo.stock_actual < cantidad:
                raise forms.ValidationError(
                    f'Stock insuficiente. Disponible: {insumo.stock_actual} unidades. '
                    f'Solicitado: {cantidad} unidades.'
                )
        
        return cleaned_data
