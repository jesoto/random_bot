import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import random

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Leer el token desde la variable de entorno
TOKEN = os.getenv("BOT_TOKEN")

# Lista de mensajes aleatorios
MESSAGES = [
    "Believe in yourself!",
    "Every day is a second chance.",
    "You are stronger than you think.",
    "Be kind, for everyone you meet is fighting a battle you know nothing about.",
    "Never give up on your dreams!",
    "Good things take time.",
    "Stay positive, work hard, and make it happen."
]

# Función para enviar un mensaje aleatorio
def send_random_message(update: Update, context: CallbackContext) -> None:
    message = random.choice(MESSAGES)
    update.message.reply_text(message)

def main():
    # Crear un objeto Updater usando el token del bot
    updater = Updater(TOKEN, use_context=True)
    
    # Obtener el dispatcher para registrar los handlers
    dispatcher = updater.dispatcher
    
    # Registrar el handler para el comando /random
    dispatcher.add_handler(CommandHandler("random", send_random_message))
    
    # Iniciar el bot
    updater.start_polling()
    
    # Mantener el bot en ejecución hasta que se presione Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
