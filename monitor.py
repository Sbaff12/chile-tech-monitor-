import os
import json
import requests
from bs4 import BeautifulSoup

# Configuración de Telegram desde las variables de entorno de GitHub Actions
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

HISTORIAL_FILE = "historial_enlaces.json"

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial(historial):
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial, f, ensure_ascii=False, indent=4)

def send_telegram_message(mensaje):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Las credenciales de Telegram no están configuradas en los secretos de GitHub.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("¡Notificación enviada a Telegram con éxito!")
        else:
            print(f"Error al enviar a Telegram: {response.text}")
    except Exception as e:
        print(f"Excepción al conectar con la API de Telegram: {e}")

def check_stores():
    print("Iniciando escaneo del radar tecnológico para componentes y dispositivos...")
    historial = cargar_historial()
    
    # Lista de elementos detectados en este ciclo de escaneo
    # Aquí puedes ir sumando las tuplas o diccionarios con tus búsquedas reales de tablets, notebooks, etc.
    hallazgos = [
        {
            "estado": "🟡 [REACONDICIONADO / OPEN BOX]",
            "titulo": "Ejemplo: Tablet de dibujo / Notebook en liquidación",
            "enlace": "https://www.superbid.cl"
        }
    ]

    nuevos_hallazgos = 0

    for item in hallazgos:
        enlace_hallazgo = item["enlace"]
        
        # Validación anti-duplicados para no spamear enlaces ya reportados
        if enlace_hallazgo not in historial:
            estado_etiqueta = item["estado"]
            titulo_hallazgo = item["titulo"]

            # Construcción limpia del mensaje para Telegram
            mensaje = (
                "🚨 *Radar Tech Activado!*\n\n" +
                estado_etiqueta + "\n" +
                "*" + titulo_hallazgo + "*\n\n" +
                "🔗 [Ver Oferta](" + enlace_hallazgo + ")"
            )
            
            send_telegram_message(mensaje)

            # Guardar en el historial para evitar alertas repetidas
            historial.append(enlace_hallazgo)
            nuevos_hallazgos += 1
        else:
            print(f"Oferta ya reportada anteriormente: {enlace_hallazgo}")

    if nuevos_hallazgos > 0:
        guardar_historial(historial)
        print(f"Se procesaron {nuevos_hallazgos} nuevos hallazgos.")
    else:
        print("Escaneo finalizado sin nuevas coincidencias no registradas. El sistema sigue vigilando.")

if __name__ == "__main__":
    check_stores()
