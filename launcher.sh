#!/bin/bash

# Configuración simple (cambia estos valores si quieres)
TARGET_USER="admin"  # Usuario objetivo (ej. "admin")
MAX_LENGTH=3  # Longitud máxima (usa 3 para encontrar "123" rápido)

echo "=== LAUNCHER BASH: BRUTE FORCE VIA PYTHON ==="
echo "Usuario objetivo: $TARGET_USER"
echo "Longitud máxima: $MAX_LENGTH"
echo "----------------------------------------"
echo "¡Asegúrate de que la API esté corriendo en otro terminal (uvicorn main:app --host 0.0.0.0 --port 8000)!"
echo "Presiona Enter para continuar..."
read -p ""

# Chequeo mínimo: Python y archivo
command -v python >/dev/null 2>&1 || { echo "Error: python no encontrado. Instala Python."; exit 1; }
[[ -f bruteforce.py ]] || { echo "Error: bruteforce.py no encontrado en la carpeta actual."; exit 1; }

# Activa venv si existe (para Windows/Git Bash)
if [[ -d "venv" ]]; then
    source venv/Scripts/activate  # En Windows/Git Bash
    echo "Entorno virtual activado."
else
    echo "No se encontró venv. Asegúrate de tener dependencias instaladas."
fi

# Llama a Python con argumentos (usa 'python' para compatibilidad Windows)
python bruteforce.py "$TARGET_USER" "$MAX_LENGTH"

start_time=$(date +%s)  # Para tiempo total (simple)
elapsed=$(( $(date +%s) - start_time ))
echo "Ataque terminado. Tiempo total aproximado: ${elapsed}s"
echo "Presiona Enter para salir..."
read -p ""