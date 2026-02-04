# Agencia-Viajes-SQLAlchemy-ejercicio
ejercicio de Sistema de gestión de reservas de viajes con Python y ORM (IDE usado: Pycharm)

# Agencia de Viajes (Backend/Consola)
Sistema de gestión de reservas desarrollado en Python, enfocado en la persistencia de datos y relaciones complejas mediante ORM.

## Características Técnicas
- **Lenguaje:** Python 3.x
- **ORM:** SQLAlchemy (Gestión de base de datos relacional).
- **Arquitectura:** Separación en Modelos (`models.py`), Conexión (`db.py`) y Lógica (`main.py`).
- **Base de Datos:** SQLite.

## Estructura de Datos
El proyecto implementa relaciones avanzadas entre tablas:
- **1:1** (Cliente - Pasaporte).
- **1:N** (Destino - Viajes).
- **N:M** (Clientes - Reservas - Viajes).

## Autor
Enrique Medina Galán
