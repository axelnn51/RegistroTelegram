import logging
from telegram.ext import Updater, MessageHandler, Filters
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ACTIVAR LOGS PARA VER ERRORES EN REPLIT
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# CONFIGURA TU TOKEN AQUÍ (manténlo privado)
TELEGRAM_TOKEN = "7758578589:AAGH3mCc7PF1huQAkVaET5Ezw-8zluz8NEY"  # ✅ Reemplaza si lo cambias

# GOOGLE SHEETS
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS = ServiceAccountCredentials.from_json_keyfile_name("bot-registro-ventas-458920-1193064cb25c.json", SCOPE)
client = gspread.authorize(CREDS)
sheet = client.open("Registro de Ventas").sheet1

def procesar_mensaje(update, context):
    texto = update.message.text.strip()
    usuario = update.message.from_user.username or update.message.from_user.first_name
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    hora = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        partes = texto.split()
        if len(partes) < 3:
            raise ValueError("Faltan partes del mensaje.")

        producto = partes[0]
        precio = partes[1]
        metodo_pago = partes[2]
        fila = [producto, precio, metodo_pago, fecha, hora, usuario]
        sheet.append_row(fila)
        update.message.reply_text("✅ Registrado con éxito.")
    except Exception as e:
        update.message.reply_text("❌ Formato inválido. Usa: Producto Precio MétodoDePago")
        logging.error(f"Error procesando mensaje: {e}")

def main():
    print("Iniciando bot...")
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, procesar_mensaje))
    updater.start_polling()
    print("Bot esperando mensajes...")
    updater.idle()

if __name__ == '__main__':
    main()
