import wikipedia
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Wikipedia ma'lumotlarini olish funksiyasi
def get_wiki_info(query):
    try:
        wikipedia.set_lang("uz")  # O'zbek tilini sozlash
        summary = wikipedia.summary(query, sentences=3)  # 3 jumlali xulosa
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ko'p ma'noli so'z: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Uzr, bu mavzu bo'yicha ma'lumot topilmadi."
    except Exception as e:
        return f"Xato yuz berdi: {str(e)}"

# /start komandasi uchun handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Wikipedia botiga xush kelibsiz! Mavzu yoki so'z kiriting, men Wikipedia'dan ma'lumot topaman.")

# Oddiy matnli xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    result = get_wiki_info(query)
    await update.message.reply_text(result)

def main():
    # Bot tokenini qo'yish
    TOKEN = "8106697853:AAGMy8g2TObSegzg8ZFYWNh8pLrdNumaGMs"
    
    # Application ob'ektini yaratish
    application = Application.builder().token(TOKEN).build()

    # Handler'larni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()