"""
Modelos de la aplicación de inventario.
Define las estructuras de datos para Insumos y Movimientos de stock.
"""
from django.db import models
from django.contrib.auth.models import User


class Insumo(models.Model):
    """
    Modelo que representa un insumo o repuesto en el inventario forestal.
    
    Attributes:
        codigo (str): Código único identificador del insumo (ej: HER-001)
        nombre (str): Nombre descriptivo del insumo
        descripcion (str): Descripción detallada del insumo (opcional)
        stock_actual (int): Cantidad actual disponible en inventario
        ubicacion (str): Ubicación física del insumo en el almacén
    """
    codigo = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Código",
        help_text="Código único del insumo (ej: HER-001)"
    )
    nombre = models.CharField(
        max_length=100, 
        verbose_name="Nombre",
        help_text="Nombre descriptivo del insumo"
    )
    descripcion = models.TextField(
        verbose_name="Descripción", 
        blank=True,
        help_text="Descripción detallada del insumo (opcional)"
    )
    stock_actual = models.IntegerField(
        default=0, 
        verbose_name="Stock Actual",
        help_text="Cantidad disponible en inventario"
    )
    ubicacion = models.CharField(
        max_length=100, 
        verbose_name="Ubicación",
        help_text="Ubicación física en el almacén"
    )

    class Meta:
        verbose_name = "Insumo"
        verbose_name_plural = "Insumos"
        ordering = ['codigo']  # Ordenar por código por defecto

    def __str__(self):
        """Representación en texto del insumo"""
        return f"{self.codigo} - {self.nombre}"


class Movimiento(models.Model):
    """
    Modelo que representa un movimiento de stock (entrada o salida).
    
    Cada movimiento registra una entrada o salida de insumos del inventario,
    manteniendo un historial completo de todas las transacciones.
    
    Attributes:
        insumo (Insumo): Insumo relacionado con este movimiento
        tipo (str): Tipo de movimiento (ENTRADA o SALIDA)
        cantidad (int): Cantidad de unidades movidas
        fecha (datetime): Fecha y hora del movimiento (auto-generada)
        usuario (User): Usuario que registró el movimiento
    """
    # Opciones para el tipo de movimiento
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),  # Ingreso de stock al inventario
        ('SALIDA', 'Salida'),    # Egreso de stock del inventario
    ]

    insumo = models.ForeignKey(
        Insumo, 
        on_delete=models.CASCADE,  # Si se elimina el insumo, se eliminan sus movimientos
        verbose_name="Insumo",
        help_text="Insumo relacionado con este movimiento"
    )
    tipo = models.CharField(
        max_length=10, 
        choices=TIPO_CHOICES, 
        verbose_name="Tipo de Movimiento",
        help_text="Tipo de movimiento: Entrada o Salida"
    )
    cantidad = models.PositiveIntegerField(
        verbose_name="Cantidad",
        help_text="Cantidad de unidades a mover"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,  # Se establece automáticamente al crear el registro
        verbose_name="Fecha",
        help_text="Fecha y hora del movimiento"
    )
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,  # Si se elimina el usuario, el movimiento se mantiene
        null=True, 
        verbose_name="Usuario Responsable",
        help_text="Usuario que registró este movimiento"
    )

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        ordering = ['-fecha']  # Ordenar por fecha descendente (más recientes primero)

    def __str__(self):
        """Representación en texto del movimiento"""
        return f"{self.tipo} - {self.insumo.nombre} ({self.cantidad} unidades)"
