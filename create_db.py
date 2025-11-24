import MySQLdb
import os
from dotenv import load_dotenv

load_dotenv()

try:
    db = MySQLdb.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        passwd=os.getenv('MYSQL_PASSWORD'),
        port=int(os.getenv('MYSQL_PORT'))
    )
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ev3backend CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print("Database 'ev3backend' created successfully (or already exists).")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    if 'db' in locals():
        db.close()
