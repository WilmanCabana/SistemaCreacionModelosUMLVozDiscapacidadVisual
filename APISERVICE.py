"""
API_SERVICE.py
Servidor FastAPI con endpoint WebSocket para procesamiento de texto
Objetivo: Recibir texto desde frontend, procesarlo y devolver resultados
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import Dict, Any
import logging


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("APISERVICE")

# Crear aplicación FastAPI
app = FastAPI(
    title="API Service con WebSocket",
    description="Servidor para procesamiento de texto en tiempo real",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  WEBSOCKET ENDPOINT

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket principal
    Recibe texto, procesa y envía resultados en tiempo real
    """
    await websocket.accept()
    logger.info("Nueva conexión WebSocket establecida")
    
    try:
        while True:
            # Recibir mensaje del frontend
            data = await websocket.receive_text()
            logger.info(f"Mensaje recibido: {data[:50]}...")
            
            try:
                # Parsear JSON si viene en ese formato
                message = json.loads(data)
                text = message.get("text", data)
                action = message.get("action", "process")
            except json.JSONDecodeError:
                # Si no es JSON, usar el texto directamente
                text = data
                action = "process"
            
            # Validar entrada
            if not text or len(text.strip()) == 0:
                await websocket.send_json({
                    "status": "error",
                    "message": "El texto está vacío"
                })
                continue
            
            # Enviar confirmación de recepción
            await websocket.send_json({
                "status": "processing",
                "message": "Procesando tu solicitud..."
            })
            
            # Procesar el texto
            #result =  classify_and_generate_diagram(text)
            result = {
                "original_text": text,
                "processed_text": text.upper(),  # Ejemplo simple de procesamiento
                "action": action
            }
            # Enviar resultado
            await websocket.send_json(result)
            logger.info("Resultado enviado exitosamente")
            
    except WebSocketDisconnect:
        logger.info("Cliente desconectado")
    except Exception as e:
        logger.error(f"Error en WebSocket: {str(e)}")
        try:
            await websocket.send_json({
                "status": "error",
                "message": f"Error del servidor: {str(e)}"
            })
        except:
            pass

# ==================== ENDPOINTS HTTP ADICIONALES ====================

@app.get("/")
async def root():
    """Endpoint raíz - Información del servicio"""
    return {
        "service": "API Service con WebSocket"
    }





