import logging
import db

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import datetime
from yandex_music import Client, DownloadInfo

TOKEN = None
my_db: db.sqlite3.Connection

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    await update.message.reply_text("Пришли пожалуйста свой токен в формате /your_token. Я его никуда не сохраню, честно-честно")
    


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""
    Отправь мне свой токен в формате /your_token\n
    Чтобы получить токен авторизации, выполните следующие действия:\n
    1. Войдите в свою учетную запись Яндекс Музыки на своем компьютере.\n
    2. В своем браузере перейдите по ссылке https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d.\n
    3. Скопируйте строку символов из адресной строки браузера, которая появляется при автоматическом перенаправлении. Она должна выглядеть примерно так: 
            AAG8XgAAAADZdiE_EO7_JoFQdTgqBZXkmGOSZeRjVlYM
это и будет Вашим токеном
    """)


# async def gllt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Echo the user message."""
#     # await update.message.reply_text("In the development")
#     if TOKEN != None:
#         url, name = func()
#         print(name)
#         await update.message.reply_audio(audio=url, title=name, performer=name, filename=name, message_effect_id=name, caption=name)
#     else:
#         await update.message.reply_text("Пришли вначале свой токен")
        


async def gllt_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.message.reply_text(update.message.text)
    global TOKEN
    TOKEN = update.message.text
    if TOKEN[0] == "/":
        TOKEN = TOKEN[1:]
    try:
        url, name = func()
        print(name)
        await update.message.reply_audio(audio=url, title=name, performer=name, filename=name, message_effect_id=name, caption=name)
    except:
        await update.message.reply_text("Некорректный токен :(")
    TOKEN = None
    


def func() -> tuple[str, str]:
    # без автор изации недоступен список треков альбома
    

    client = Client(TOKEN).init()

    playlist = client.users_likes_tracks()
    arr = []

    for i in playlist:
        # print(i.fetch_track().title)
        time = datetime.datetime.strptime(i['timestamp'][:-6], '%Y-%m-%dT%H:%M:%S')
        arr = [time, i['album_id'], i['id'], i.fetch_track().title]
        break

    # arr.sort(reverse=True)

    for i in client.tracks_download_info(arr[2], True):
        # print(i)
        if i["codec"] == "mp3":
            return i["direct_link"], arr[3]


def main() -> None:
    global my_db
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("7066146595:AAGEIuIPj9pRUiNtH2_hM0jEOeT5AZv5WfQ").build()
    
    # Create DB users where id - TelegramID, token - user's token
    my_db = db.create_connection("./users.db")
    buf = """
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL
        );
    """
    db.execute_query(my_db, buf)
    
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # application.add_handler(CommandHandler("last_liked", gllt_command))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gllt_command))
    application.add_handler(MessageHandler(filters.TEXT, gllt_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()