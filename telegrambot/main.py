from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from database import get_all_players, get_player  

load_dotenv()
TOKEN = os.getenv('TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Привітання при запуску бота"""
    await update.message.reply_text(f"Привіт, {update.effective_user.first_name}!\nЯ бот для перегляду рейтингу гравців.")

async def rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отримання рейтингу всіх гравців"""
    players = get_all_players()
    
    if not players:
        await update.message.reply_text("⚠️ Рейтинг поки що порожній.")
        print("Рейтинг порожній!")
        return
    
    message = "🏆 Рейтинг гравців:\n"
    for i, (name, level, points, playtime) in enumerate(players, 1):
        message += f"{i}. {name} - Рівень: {level}, Очки: {points}, Час: {playtime} хв.\n"
    
    await update.message.reply_text(message)
    print("Рейтинг надіслано!")

async def get_player_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отримання інформації про конкретного гравця"""
    if not context.args:
        await update.message.reply_text("⚠ Вкажіть ім'я гравця: /player <ім'я>")
        return

    username = context.args[0]
    player = get_player(username)

    if not player:
        await update.message.reply_text(f"❌ Гравця з іменем {username} не знайдено.")
        return

    name, level, points, playtime = player
    message = f"🎮 Інформація про гравця {name}:\n\n"
    message += f"🔹 Рівень: {level}\n"
    message += f"🔹 Очки: {points}\n"
    message += f"🔹 Час у грі: {playtime} хв."

    await update.message.reply_text(message)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rating", rating))
app.add_handler(CommandHandler("player", get_player_info))

app.run_polling()
