import os
import json
import requests
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
HISTORIAL_FILE = "historial_enlaces.json"

# Palabras clave de electrónica media-alta (puedes agregar o quitar las que quieras)
PALABRAS_CLAVE = [
    "notebook", "laptop", "rtx", "radeon", "monitor", "oled", "ips",
    "wacom", "huion", "xp-pen", "ipad", "tablet", "ryzen", "core i7",
    "core i9", "core ultra", "televisor", "smart tv", "ssd", "nvme",
    "ram", "ddr5", "sennheiser", "sony", "audifonos", "tarjeta de video"
]

# Descuento mínimo real exigido para que te mande alerta (ej: 25%)
DESCUENTO_MINIMO = 25

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "es-CL,es;q=0.9"
}

def cargar_historial():
    if os.path.exists(HISTORIAL_FILE):
        try:
            with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def guardar_historial(historial):
    # Guardamos los últimos 500 enlaces para que el archivo no crezca infinito
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(historial[-500:], f, ensure_ascii=False, indent=2)

def enviar_telegram(mensaje):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Credenciales de Telegram no configuradas.")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        r = requests.post(url, json=payload, timeout=15)
        return r.status_code == 200
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")
        return False

def cumple_filtro(titulo):
    titulo_lower = titulo.lower()
    return any(palabra in titulo_lower for palabra in PALABRAS_CLAVE)

def buscar_ofertas_solotodo():
    """Consulta la API pública de ofertas reales de SoloTodo Chile"""
    ofertas = []
    # Categorías clave de SoloTodo: Notebooks (1), Monitores (4), Tarjetas de Video (2), Tablets (32), Televisores (11)
    categorias = [1, 4, 2, 32, 11]
    
    for cat in categorias:
        url_api = f"https://publicapi.solotodo.com/products/browse/?categories={cat}&ordering=-discount&page_size=15"
        try:
            resp = requests.get(url_api, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            datos = resp.json()
            for item in datos.get("results", []):
                producto = item.get("product", {})
                nombre = producto.get("name", "")
                slug = producto.get("slug", "")
                prod_id = producto.get("id", "")
                
                pricing = item.get("pricing", {})
                precio_oferta = pricing.get("offer_price")
                precio_normal = pricing.get("normal_price")
                
                if not (nombre and prod_id and precio_oferta and precio_normal):
                    continue
                
                precio_oferta = float(precio_oferta)
                precio_normal = float(precio_normal)
                
                if precio_normal <= precio_oferta:
                    continue
                
                descuento = round(((precio_normal - precio_oferta) / precio_normal) * 100)
                
                if descuento >= DESCUENTO_MINIMO and cumple_filtro(nombre):
                    enlace_directo = f"https://www.solotodo.cl/products/{prod_id}-{slug}"
                    ofertas.append({
                        "titulo": nombre,
                        "precio_oferta": f"${int(precio_oferta):,}".replace(",", "."),
                        "precio_normal": f"${int(precio_normal):,}".replace(",", "."),
                        "descuento": descuento,
                        "enlace": enlace_directo
                    })
        except Exception as e:
            print(f"Error consultando categoría {cat}: {e}")
            
    return ofertas

def ejecutar_radar():
    print("Iniciando escaneo de ofertas reales de electrónica media-alta...")
    historial = cargar_historial()
    nuevos_enviados = 0

    ofertas_encontradas = buscar_ofertas_solotodo()
    print(f"Productos candidatos encontrados en el escaneo: {len(ofertas_encontradas)}")

    for oferta in ofertas_encontradas:
        enlace = oferta["enlace"]
        if enlace in historial:
            continue

        mensaje = (
            f"🔥 <b>OFERTA REAL DETECTADA (-{oferta['descuento']}%)</b> 🔥\n\n"
            f"💻 <b>{oferta['titulo']}</b>\n"
            f"💰 Precio Oferta: <b>{oferta['precio_oferta']}</b>\n"
            f"🏷️ Precio Normal: <s>{oferta['precio_normal']}</s>\n\n"
            f"🔗 <a href='{enlace}'>Ver producto y tiendas aquí</a>"
        )

        if enviar_telegram(mensaje):
            print(f"Enviada: {oferta['titulo']} (-{oferta['descuento']}%)")
            historial.append(enlace)
            nuevos_enviados += 1

    if nuevos_enviados > 0:
        guardar_historial(historial)
        print(f"Escaneo finalizado. {nuevos_enviados} alerta(s) nueva(s) enviada(s).")
    else:
        print("Escaneo finalizado. Sin ofertas nuevas sobre el umbral en este ciclo.")

if __name__ == "__main__":
    ejecutar_radar()
