from django.db import models
from django.contrib.auth.models import User

class Insumo(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(verbose_name="Descripción", blank=True)
    stock_actual = models.IntegerField(default=0, verbose_name="Stock Actual")
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, verbose_name="Insumo")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo de Movimiento")
    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuario Responsable")

    def __str__(self):
        return f"{self.tipo} - {self.insumo.nombre} ({self.cantidad})"
