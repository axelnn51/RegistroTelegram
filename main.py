import os
import json
from telegram.ext import Updater, MessageHandler, Filters
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# CONFIGURACIÓN DEL BOT
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

# CONFIGURACIÓN GOOGLE SHEETS
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
json_creds = json.loads(os.environ["GOOGLE_CREDS_JSON"])
CREDS = ServiceAccountCredentials.from_json_keyfile_dict(json_creds, SCOPE)
client = gspread.authorize(CREDS)
sheet = client.open("Registro de Ventas").sheet1

def procesar_mensaje(update, context):
    texto = update.message.text.strip()
    usuario = update.message.from_user.username or update.message.from_user.first_name
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        partes = texto.split()
        producto = partes[0]
        precio = partes[1]
        metodo_pago = partes[2]
        fila = [producto, precio, metodo_pago, fecha, hora, usuario]
        sheet.append_row(fila)
        update.message.reply_text("✅ Registrado con éxito.")
    except Exception as e:
        update.message.reply_text("❌ Usa: Producto Precio MetodoPago")
        print(f"Error: {e}")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, procesar_mensaje))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

