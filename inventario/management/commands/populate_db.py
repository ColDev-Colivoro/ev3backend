from django.core.management.base import BaseCommand
from inventario.models import Insumo, Movimiento
from django.contrib.auth import get_user_model
from django.utils import timezone

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para Insumo y Movimiento'

    def handle(self, *args, **options):
        # Crear usuario de prueba si no existe
        User = get_user_model()
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(username='testuser', password='testpass')
            self.stdout.write(self.style.SUCCESS('Usuario de prueba creado'))

        # Crear Insumo de ejemplo
        insumo, created = Insumo.objects.get_or_create(
            codigo='INS-001',
            defaults={
                'nombre': 'Ejemplo Insumo',
                'descripcion': 'Insumo de prueba para la aplicación',
                'stock_actual': 100,
                'ubicacion': 'Almacén 1',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Insumo creado'))
        else:
            self.stdout.write('Insumo ya existía')

        # Crear Movimiento de ejemplo (Salida)
        movimiento, created = Movimiento.objects.get_or_create(
            insumo=insumo,
            tipo='Salida',
            cantidad=10,
            fecha=timezone.now(),
            usuario=User.objects.get(username='testuser')
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Movimiento creado'))
        else:
            self.stdout.write('Movimiento ya existía')
