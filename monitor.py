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
    print("Iniciando escaneo del radar tecnológico (Quiebras, Remates y Tiendas de Descuentos Reales)...")
    historial = cargar_historial()
    
    # Fuentes combinadas: Quiebras/Remates + Tiendas de tecnología con ofertas reales
    hallazgos = [
        {
            "estado": "🏛️ [LIQUIDACIÓN / QUIEBRA EMPRESARIAL]",
            "titulo": "Superbid: Lotes de tecnología y notebooks en liquidación",
            "enlace": "https://www.superbid.cl"
        },
        {
            "estado": "🏛️ [LIQUIDACIÓN / QUIEBRA EMPRESARIAL]",
            "titulo": "Superbid: Lotes de tecnología y notebooks en liquidación",
            "enlace": "https://www.superbid.cl"
        },
        {
            "estado": "🔨 [REMATE JUDICIAL / LIQUIDACIÓN EMPRESAS]",
            "titulo": "Macal: Remates online de tecnología, equipos y saldos",
            "enlace": "https://www.macal.cl"
        },
        {
            "estado": "💻 [OFERTAS REALES / OUTLET TECH]",
            "titulo": "SP Digital: Liquidaciones web y saldos de componentes/notebooks",
            "enlace": "https://www.spdigital.cl"
        },
        {
            "estado": "⚡ [LIQUIDACIÓN DE COMPONENTES]",
            "titulo": "PC Factory: Sección de ofertas y outlet tecnológico",
            "enlace": "https://www.pcfactory.cl/outlet"
        }
    ]
        {
            "estado": "💻 [OFERTAS REALES / OUTLET TECH]",
            "titulo": "SP Digital: Liquidaciones web y saldos de componentes/notebooks",
            "enlace": "https://www.spdigital.cl"
        },
        {
            "estado": "⚡ [LIQUIDACIÓN DE COMPONENTES]",
            "titulo": "PC Factory: Sección de ofertas y outlet tecnológico",
            "enlace": "https://www.pcfactory.cl/outlet"
        }
    ]

    nuevos_hallazgos = 0

    for item in hallazgos:
        enlace_hallazgo = item["enlace"]
        
        # Validación anti-duplicados para no spamear enlaces ya reportados
        if enlace_hallazgo not in historial:
            estado_etiqueta = item["estado"]
            titulo_hallazgo = item["titulo"]

            # Construcción limpia y segura del mensaje
            mensaje = (
                "🚨 *Radar Tech - Alerta de Oportunidad!*\n\n" +
                estado_etiqueta + "\n" +
                "*" + titulo_hallazgo + "*\n\n" +
                "🔗 [Ver Oportunidad](" + enlace_hallazgo + ")"
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
        print("Escaneo finalizado. Sin nuevas alertas en este ciclo.")

if __name__ == "__main__":
    check_stores()
