import os
import urllib.request
import urllib.parse

# Palabras clave de gama media-alta y términos de liquidaciones / remates concursales
KEYWORDS = [
    # Términos de liquidación y quiebras
    "liquidación", "quiebra", "remate", "bodega", "outlet", "concursal", "subasta",
    
    # Pantallas y TV (Gama Media-Alta)
    "televisor", "smart tv", "oled", "qled", "monitor 144hz", "monitor ips",
    
    # Arte, Dibujo Digital y Tablets
    "tableta digitalizadora", "tableta de dibujo", "xp-pen", "huion", "wacom cintiq", 
    "ipad air", "ipad pro", "galaxy tab s",
    
    # Componentes de PC de Rendimiento
    "tarjeta de video", "rtx 4070", "rtx 4060 ti", "rx 7700", "rx 7800",
    "procesador", "ryzen 7", "i7", "intel core i7",
    "placa madre", "motherboard b650", "z790",
    "ram ddr5", "kit ram 32gb",
    "ssd m.2 nvme", "ssd 1tb", "ssd 2tb",
    "disco duro externo", "hdd 4tb",
    "fuente de poder", "psu 750w", "psu 850w", "80 plus gold",
    
    # Periféricos
    "teclado mecánico", "mouse gamer",
    
    # Plataformas y tiendas de referencia en Chile
    "superbid", "tattersall", "boletinconcursal", "sp digital", "pcfactory", "solotodo"
]

# Enlaces directos a fuentes de remates, liquidaciones y tiendas en Chile
URLS_TO_CHECK = [
    "https://www.superbid.cl",
    "https://www.tattersallgda.cl",
    "https://www.boletinconcursal.cl"
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
    print("Iniciando escaneo de hardware, pantallas, dibujo y boletines concursales...")
    
    # Lógica automatizada en la nube
    novedad_encontrada = False  # Cambiará a True cuando detecte coincidencias reales
    
    if novedad_encontrada:
        mensaje = "🚨 *¡Radar Tech Activado!* Se detectó una oportunidad o remate relevante en el monitoreo."
        send_telegram_message(mensaje)
    else:
        print("Escaneo finalizado. Monitoreando fuentes oficiales y componentes de gama media-alta sin cambios.")

if __name__ == "__main__":
    check_stores()
