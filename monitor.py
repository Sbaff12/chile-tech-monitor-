import os
import json
import requests

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
        json.dump(historial, f, ensure_ascii=False, indent=2)

def enviar_telegram(mensaje):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Las credenciales de Telegram no están configuradas en los secretos de GitHub.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        respuesta = requests.post(url, json=payload, timeout=15)
        if respuesta.status_code == 200:
            print("¡Notificación enviada a Telegram con éxito!")
            return True
        else:
            print(f"Error al enviar a Telegram: {respuesta.status_code} - {respuesta.text}")
            return False
    except Exception as e:
        print(f"Excepción al conectar con Telegram: {e}")
        return False

def ejecutar_radar():
    print("Iniciando escaneo del radar tecnológico (Quiebras, Remates y Tiendas de Descuentos Reales)...")
    historial = cargar_historial()
    nuevos_enviados = 0

    hallazgos = [
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

    for item in hallazgos:
        enlace = item["enlace"]
        if enlace in historial:
            print(f"Oferta ya reportada anteriormente: {enlace}")
            continue

        mensaje = (
            f"🚨 <b>RADAR TECH QUINTA REGIÓN</b> 🚨\n\n"
            f"{item['estado']}\n"
            f"📌 <b>{item['titulo']}</b>\n\n"
            f"🔗 <a href='{enlace}'>Ver publicación aquí</a>"
        )

        if enviar_telegram(mensaje):
            historial.append(enlace)
