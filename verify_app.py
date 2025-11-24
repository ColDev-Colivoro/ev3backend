import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ev3backend.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Insumo, Movimiento

def verify():
    print("--- Verifying Models ---")
    # Create User
    user, created = User.objects.get_or_create(username='testuser', email='test@example.com')
    if created:
        user.set_password('password')
        user.save()
        print("Test user created.")
    else:
        print("Test user already exists.")

    # Create Insumo
    insumo, created = Insumo.objects.get_or_create(
        codigo='INS-001',
        defaults={
            'nombre': 'Test Insumo',
            'descripcion': 'Descripcion de prueba',
            'stock_actual': 100,
            'ubicacion': 'Bodega 1'
        }
    )
    print(f"Insumo created: {insumo}")

    # Create Movimiento
    movimiento = Movimiento.objects.create(
        insumo=insumo,
        tipo='SALIDA',
        cantidad=10,
        usuario=user
    )
    print(f"Movimiento created: {movimiento}")

    # Verify Stock Update (Logic is in View, not Model save method in this simple implementation, 
    # but let's check if we can simulate the view logic or just check model integrity)
    # The view logic updates the stock. Let's verify the view.

    print("\n--- Verifying Views ---")
    c = Client()
    
    # Login
    login_success = c.login(username='testuser', password='password')
    print(f"Login successful: {login_success}")

    # Access Insumo List
    response = c.get('/')
    print(f"Insumo List Status: {response.status_code}")
    if response.status_code == 200:
        print("Insumo List accessible.")
    else:
        print("Failed to access Insumo List.")

    # Access Create Insumo
    response = c.get('/insumo/nuevo/')
    print(f"Create Insumo Page Status: {response.status_code}")

    print("\n--- Verification Complete ---")

if __name__ == '__main__':
    verify()
