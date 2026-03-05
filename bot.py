import telebot
import os
from flask import Flask
from threading import Thread

# Configuración
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

# Verificar que las variables existen
if not BOT_TOKEN or not ADMIN_CHAT_ID:
    print("❌ ERROR: Faltan las variables BOT_TOKEN o ADMIN_CHAT_ID")
    print("Ve a Tools → Secrets y agrégalas")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# Flask para mantener el bot activo
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot de BakeBalance funcionando correctamente"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Manejador de mensajes
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Información del usuario
        user_name = message.from_user.first_name or "Usuario"
        username = f"@{message.from_user.username}" if message.from_user.username else "Sin username"
        user_id = message.from_user.id

        # Formato del mensaje
        notification = f"""
🔔 NUEVO MENSAJE - BakeBalance

👤 Nombre: {user_name}
📱 Username: {username}
🆔 ID: {user_id}

💬 Mensaje:
{message.text}

━━━━━━━━━━━━━━━━━
"""

        # Enviar al grupo
        bot.send_message(ADMIN_CHAT_ID, notification)

        # Respuesta automática
        respuesta = """¡Gracias por contactar a BakeBalance! 🍰

Hemos recibido tu mensaje y te responderemos pronto.

⏰ Horario de atención:
Lunes a Sábado, 9:00 AM - 6:00 PM (GMT-5)
"""
        bot.reply_to(message, respuesta)

        print(f"✅ Mensaje procesado de: {user_name}")

    except Exception as e:
        print(f"❌ Error: {e}")

# Iniciar
if __name__ == '__main__':
    print("🤖 Bot de BakeBalance iniciado...")
    print(f"📱 Escuchando mensajes...")

    # Flask en thread separado
    Thread(target=run_flask, daemon=True).start()

    # Iniciar bot
    bot.infinity_polling()
