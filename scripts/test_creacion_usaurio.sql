CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'Django_123';
GRANT ALL PRIVILEGES ON inventario_escolar.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
