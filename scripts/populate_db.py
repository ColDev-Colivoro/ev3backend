"""
Script para poblar la base de datos con datos de ejemplo.
Ejecuta el comando Django 'populate_db' que crea usuarios, insumos y movimientos de prueba.
"""
import os
import sys
import django

# Configurar el path para Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ev3backend.settings')

# Inicializar Django
django.setup()

# Importar y ejecutar el comando
from django.core.management import call_command

if __name__ == '__main__':
    print("Poblando la base de datos con datos de ejemplo...\n")
    call_command('populate_db')
