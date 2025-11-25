from django.core.management.base import BaseCommand
from inventario.models import Insumo, Movimiento
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de ejemplo para Insumo y Movimiento'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Crear usuarios de prueba
        self.stdout.write(self.style.WARNING('Creando usuarios...'))
        
        # Usuario administrador
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                password='admin123',
                email='admin@inventario.com',
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superusuario "admin" creado (password: admin123)'))
        
        # Usuario de prueba regular
        if not User.objects.filter(username='testuser').exists():
            User.objects.create_user(
                username='testuser',
                password='testpass',
                email='test@inventario.com',
                first_name='Usuario',
                last_name='Prueba'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario "testuser" creado (password: testpass)'))
        
        # Usuario operador
        if not User.objects.filter(username='operador').exists():
            User.objects.create_user(
                username='operador',
                password='operador123',
                email='operador@inventario.com',
                first_name='Juan',
                last_name='Pérez'
            )
            self.stdout.write(self.style.SUCCESS('✓ Usuario "operador" creado (password: operador123)'))
        
        # Crear insumos de ejemplo
        self.stdout.write(self.style.WARNING('\nCreando insumos...'))
        
        insumos_data = [
            {
                'codigo': 'HER-001',
                'nombre': 'Motosierra STIHL MS 381',
                'descripcion': 'Motosierra profesional para trabajos forestales pesados',
                'stock_actual': 15,
                'ubicacion': 'Almacén Principal - Sección A1'
            },
            {
                'codigo': 'HER-002',
                'nombre': 'Hacha Forestal 3.5kg',
                'descripcion': 'Hacha de acero forjado con mango de fibra de vidrio',
                'stock_actual': 45,
                'ubicacion': 'Almacén Principal - Sección A2'
            },
            {
                'codigo': 'EPP-001',
                'nombre': 'Casco de Seguridad Forestal',
                'descripcion': 'Casco con protección facial y auditiva',
                'stock_actual': 30,
                'ubicacion': 'Almacén EPP - Estante B1'
            },
            {
                'codigo': 'EPP-002',
                'nombre': 'Guantes Anti-corte',
                'descripcion': 'Guantes de protección nivel 5 para trabajo forestal',
                'stock_actual': 120,
                'ubicacion': 'Almacén EPP - Estante B2'
            },
            {
                'codigo': 'REP-001',
                'nombre': 'Cadena para Motosierra 20"',
                'descripcion': 'Cadena de repuesto compatible con STIHL MS 381',
                'stock_actual': 25,
                'ubicacion': 'Almacén Repuestos - Cajón C1'
            },
            {
                'codigo': 'REP-002',
                'nombre': 'Filtro de Aire para Motosierra',
                'descripcion': 'Filtro de aire de alta eficiencia',
                'stock_actual': 50,
                'ubicacion': 'Almacén Repuestos - Cajón C2'
            },
            {
                'codigo': 'COM-001',
                'nombre': 'Aceite para Cadena 1L',
                'descripcion': 'Aceite biodegradable para lubricación de cadenas',
                'stock_actual': 200,
                'ubicacion': 'Almacén Químicos - Estante D1'
            },
            {
                'codigo': 'COM-002',
                'nombre': 'Combustible Mezcla 2T',
                'descripcion': 'Mezcla preparada gasolina/aceite 50:1',
                'stock_actual': 150,
                'ubicacion': 'Almacén Químicos - Estante D2'
            },
        ]
        
        insumos_creados = []
        for data in insumos_data:
            insumo, created = Insumo.objects.get_or_create(
                codigo=data['codigo'],
                defaults=data
            )
            if created:
                insumos_creados.append(insumo)
                self.stdout.write(self.style.SUCCESS(f'✓ Insumo "{insumo.nombre}" creado'))
            else:
                self.stdout.write(f'  Insumo "{insumo.nombre}" ya existía')
        
        # Crear movimientos de ejemplo
        if insumos_creados:
            self.stdout.write(self.style.WARNING('\nCreando movimientos de ejemplo...'))
            
            usuario_admin = User.objects.get(username='admin')
            usuario_operador = User.objects.get(username='operador')
            
            movimientos_data = [
                # Entradas iniciales
                {
                    'insumo': Insumo.objects.get(codigo='HER-001'),
                    'tipo': 'ENTRADA',
                    'cantidad': 10,
                    'fecha': timezone.now() - timedelta(days=30),
                    'usuario': usuario_admin
                },
                {
                    'insumo': Insumo.objects.get(codigo='EPP-001'),
                    'tipo': 'ENTRADA',
                    'cantidad': 50,
                    'fecha': timezone.now() - timedelta(days=25),
                    'usuario': usuario_admin
                },
                # Salidas
                {
                    'insumo': Insumo.objects.get(codigo='EPP-001'),
                    'tipo': 'SALIDA',
                    'cantidad': 20,
                    'fecha': timezone.now() - timedelta(days=15),
                    'usuario': usuario_operador
                },
                {
                    'insumo': Insumo.objects.get(codigo='COM-001'),
                    'tipo': 'SALIDA',
                    'cantidad': 30,
                    'fecha': timezone.now() - timedelta(days=10),
                    'usuario': usuario_operador
                },
                # Entradas recientes
                {
                    'insumo': Insumo.objects.get(codigo='HER-001'),
                    'tipo': 'ENTRADA',
                    'cantidad': 5,
                    'fecha': timezone.now() - timedelta(days=5),
                    'usuario': usuario_admin
                },
                {
                    'insumo': Insumo.objects.get(codigo='REP-001'),
                    'tipo': 'ENTRADA',
                    'cantidad': 15,
                    'fecha': timezone.now() - timedelta(days=3),
                    'usuario': usuario_admin
                },
            ]
            
            for mov_data in movimientos_data:
                movimiento, created = Movimiento.objects.get_or_create(**mov_data)
                if created:
                    self.stdout.write(self.style.SUCCESS(
                        f'✓ Movimiento {mov_data["tipo"]} de {mov_data["cantidad"]} unidades '
                        f'para "{mov_data["insumo"].nombre}"'
                    ))
        
        # Resumen final
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ Base de datos poblada exitosamente'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'\nUsuarios creados: {User.objects.count()}')
        self.stdout.write(f'Insumos creados: {Insumo.objects.count()}')
        self.stdout.write(f'Movimientos creados: {Movimiento.objects.count()}')
        
        self.stdout.write(self.style.WARNING('\n--- Credenciales de Acceso ---'))
        self.stdout.write('Superusuario: admin / admin123')
        self.stdout.write('Usuario prueba: testuser / testpass')
        self.stdout.write('Operador: operador / operador123')
