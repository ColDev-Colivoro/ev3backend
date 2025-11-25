import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

# Leer el archivo SQL
with open('create_tables.sql', 'r', encoding='utf-8') as f:
    sql_script = f.read()

# Dividir el script en comandos individuales
sql_commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]

try:
    # Conectar a la base de datos
    db = MySQLdb.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        passwd=os.getenv('MYSQL_PASSWORD', ''),
        db='ev3backend',  # Nombre de la base de datos
        port=int(os.getenv('MYSQL_PORT', '3306'))
    )
    cursor = db.cursor()
    
    print("Ejecutando comandos SQL...")
    for i, command in enumerate(sql_commands, 1):
        if command:
            try:
                cursor.execute(command)
                print(f"✓ Comando {i} ejecutado correctamente")
            except Exception as e:
                print(f"✗ Error en comando {i}: {e}")
                print(f"  Comando: {command[:100]}...")
    
    db.commit()
    print("\n¡Todas las tablas fueron creadas exitosamente!")
    
except Exception as e:
    print(f"Error conectando a la base de datos: {e}")
finally:
    if 'db' in locals():
        db.close()
