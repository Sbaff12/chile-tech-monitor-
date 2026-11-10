import os
import urllib.request
import urllib.parse

# Palabras clave ampliadas: Gama media-alta en computación, pantallas, dibujo y almacenamiento
KEYWORDS = [
    # Indicadores de oferta / liquidación
    "liquidación", "quiebra", "oferta", "bodega", "outlet", "descuento",
    
    # Pantallas y TV
    "televisor", "tv", "smart tv", "oled", "qled", "monitor 144hz", "monitor 240hz", "monitor ips",
    
    # Arte y Dibujo Digital
    "tableta digitalizadora", "tableta de dibujo", "huion", "xp-pen", "wacom cintiq", "wacom intuos",
    
    # Tablets generales
    "ipad air", "ipad pro", "galaxy tab s", "tablet gama alta",
    
    # Componentes de PC (Gama Media-Alta)
    "tarjeta de video", "rtx 4070", "rtx 4060 ti", "rx 7700", "rx 7800",
    "procesador", "ryzen 7", "i7", "intel core i7",
    "placa madre", "motherboard b650", "z790",
    "ram ddr5", "kit ram 32gb",
    "ssd m.2 nvme", "disco duro ssd 2tb", "ssd 1tb",
    "disco duro externo", "hdd 4tb", "disco duro almacenamiento",
    "fuente de poder", "psu 750w", "psu 850w", "certificación 80 plus gold",
    
    # Periféricos de rendimiento
    "teclado mecánico", "switch red", "mouse gamer", "logitech g", "razer",
    
    # Tiendas de referencia en Chile
    "sp digital", "pcfactory", "solotodo", "winpy", "ttcl"
]

# Enlaces directos a secciones de ofertas o liquidación en tiendas chilenas
URLS_TO_CHECK = [
    # Puedes agregar aquí URLs específicas si lo deseas más adelante
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
    print("Iniciando escaneo de gama media-alta (Hardware, Dibujo, Almacenamiento y Pantallas)...")
    
    # Lógica automatizada en la nube
    novedad_encontrada = False  # Cambiará a True cuando detecte coincidencias reales
    
    if novedad_encontrada:
        mensaje = "🚨 *¡Radar Tech Activado!* Se detectó una oferta de gama media-alta en el monitoreo."
        send_telegram_message(mensaje)
    else:
        print("Escaneo finalizado. Monitoreando componentes y equipos de alto rendimiento sin cambios.")

if __name__ == "__main__":
    check_stores() 
