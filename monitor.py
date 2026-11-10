import urllib.request
import json
import os

# Palabras clave que el script buscará en los sitios o boletines
KEYWORDS = ["quiebra", "liquidación", "sp digital", "computación", "valparaíso"]

# Puedes agregar aquí las páginas web o RSS que quieras monitorear
URLS_TO_CHECK = [
    # Aquí irán más adelante las páginas de las tiendas de la V Región o boletines
]

def check_stores():
    print("Iniciando escaneo de tiendas y boletines...")
    # Aquí irá la lógica principal de búsqueda y comparación de precios/alertas
    print("Escaneo finalizado. Sin novedades por ahora.")

if __name__ == "__main__":
    check_stores()
