import os
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACE_TOKEN')

# URL del modelo de Hugging Face
HUGGINGFACE_MODEL_URL = "https://huggingface.co/TurkuNLP/gpt3-finnish-large"

# Función para obtener respuestas del modelo de Hugging Face
def get_huggingface_response(prompt):
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_TOKEN}"
    }
    response = requests.post(HUGGINGFACE_MODEL_URL, headers=headers, json={"inputs": prompt})

    # Manejo de errores en la respuesta
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Error {response.status_code}: {response.text}"}

# Función para manejar los mensajes del usuario
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    bot_response = get_huggingface_response(user_message)

    # Manejar la respuesta del modelo
    if isinstance(bot_response, list) and "generated_text" in bot_response[0]:
        response_text = bot_response[0]["generated_text"]
    elif "error" in bot_response:
        response_text = bot_response["error"]
    else:
        response_text = "Lo siento, no pude obtener una respuesta."

    update.message.reply_text(response_text)

# Configuración del bot de Telegram
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Agregar manejadores de mensajes
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
