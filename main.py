from fastapi import FastAPI, Request
import openai
import os

app = FastAPI()

# Tu clave de OpenAI vendrá de una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    
    # Mensaje de WhatsApp recibido
    mensaje = data.get("Body", "")
    numero = data.get("From", "")
    
    # Si no hay mensaje, no hacemos nada
    if not mensaje:
        return {"message": "Mensaje vacío"}

    # Llamada a OpenAI con modelo GPT-4o mini
    respuesta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asistente virtual amigable que ayuda a responder dudas."},
            {"role": "user", "content": mensaje}
        ]
    )

    mensaje_respuesta = respuesta['choices'][0]['message']['content']
    
    # Twilio espera una respuesta directa, la devolveremos como texto
    return {
        "message": mensaje_respuesta
    }
