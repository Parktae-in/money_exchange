from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
import logging

load_dotenv()
TOKEN = os.getenv("TOKEN")
#CHAT_ID = 6366489629

f = open('telegram_chatid.txt', 'r')
CHAT_ID = int(f.read().strip())

print(CHAT_ID)

#로그 출력
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def help_command(update, context):
    await update.message.reply_text("도움말 입니다.")

async def test_command(update, context):
    #이미지 전송
    await context.bot.send_photo(chat_id=6366489629, photo=open("google_logo.png", "rb"))
    await update.message.reply_text("테스트 입니다.")

async def echo(update, context):
    if update.message.text.find("비디오 전송") >= 0:
        await context.bot.send_video(chat_id=CHAT_ID, video=open("videotest.mp4", "rb"), write_timeout=30000)
    if update.message.text.find("오디오 전송") >= 0:
        await context.bot.send_audio(chat_id=CHAT_ID, audio=open("audio.wav", "rb"), write_timeout=30000)
    if update.message.text.find("스티커 전송") >= 0:
        await context.bot.send_sticker(chat_id=CHAT_ID, sticker=open("google_logo.png", "rb"), write_timeout=30000)
    await update.message.reply_text(update.message.text)

application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("test", test_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

#내부적 쓰레드로 동작
application.run_polling(allowed_updates=Update.ALL_TYPES)