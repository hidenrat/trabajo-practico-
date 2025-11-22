#!/bin/bash

echo "Acordar que para iniciarlo, antes de debe dar los permisos asi: 'chmod +x iniciar_servidores.sh'"

# Este script inicia los servidores de Frontend y Backend en segundo plano.

# --- 1. Iniciando SERVIDOR BACKEND (API - Puerto 5003) ---
# El '&' al final pone el proceso en segundo plano.
python backend/app_back.py & 
BACKEND_PID=$! # Guarda el ID del proceso del backend para poder detenerlo

echo "Backend iniciado en Puerto 5003 (PID: $BACKEND_PID)"
sleep 1 # Pausa para dar tiempo a iniciar

# --- 2. Iniciando SERVIDOR FRONTEND (WEB - Puerto 5002) ---
python frontend/app.py &
FRONTEND_PID=$! # Guarda el ID del proceso del frontend

echo "Frontend iniciado en Puerto 5002 (PID: $FRONTEND_PID)"
echo "--------------------------------------------------------"
echo "Presiona [Enter] para detener ambos servidores..."

# Espera a que el usuario presione Enter
read

# Detiene los procesos usando el PID guardado
kill $BACKEND_PID
kill $FRONTEND_PID

echo "Servidores detenidos. ¡Finalizado!"
