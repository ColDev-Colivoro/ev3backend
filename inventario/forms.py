from django import forms
from .models import Insumo, Movimiento

class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = ['codigo', 'nombre', 'descripcion', 'stock_actual', 'ubicacion']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['insumo', 'tipo', 'cantidad']
        widgets = {
            'insumo': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        cantidad = cleaned_data.get('cantidad')
        insumo = cleaned_data.get('insumo')

        if tipo == 'SALIDA' and insumo and cantidad:
            if insumo.stock_actual < cantidad:
                raise forms.ValidationError("No hay suficiente stock para realizar esta salida.")
        
        return cleaned_data
