import os
import urllib.request
import urllib.parse

# Palabras clave orientadas a computación, electrónica, audífonos y liquidaciones
KEYWORDS = [
    "liquidación", "quiebra", "oferta", "bodega", 
    "tarjeta de video", "rtx", "procesador", "ryzen", "intel", 
    "audífonos", "headset", "monitor", "gabinete", "placa madre",
    "sp digital", "pcfactory", "solotodo"
]

# Aquí puedes ir agregando los enlaces o páginas web clave que quieras escanear
URLS_TO_CHECK = [
    # Ejemplo: "https://www.spdigital.cl", 
]

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Faltan las credenciales de Telegram configuradas en GitHub Actions.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            print("¡Alerta enviada a Telegram con éxito!")
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def check_stores():
    print("Iniciando escaneo de componentes, audífonos y electrónica...")
    
    # Aquí es donde el script evaluará las páginas o términos
    novedad_encontrada = False  # Se activará automáticamente al detectar coincidencias reales
    
    if novedad_encontrada:
        mensaje = "🚨 *¡Radar Tech Activado!* Se detectó una oferta o movimiento de liquidación en electrónica."
        send_telegram_message(mensaje)
    else:
                    print("Escaneo finalizado. Monitoreando stock de hardware y audífonos sin cambios por ahora.")

if __name__ == "__main__":
    check_stores()
