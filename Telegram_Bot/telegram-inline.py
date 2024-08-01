from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler
from dotenv import load_dotenv
from Money_Exchange.money_exchange_rate import google_money_exchange_rate
import os
import logging
import re
from uuid import uuid4

load_dotenv()
TOKEN = os.getenv("TOKEN")

f = open('telegram_chatid.txt', 'r')
CHAT_ID = int(f.read().strip())

print(CHAT_ID)

#로그 출력
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

#번환 가능 화폐
money_names = ["달러", "엔", "위안", "유로"]

async def inline_query(update, context):
    query = update.inline_query.query
    if query == "":
        return
    print(f">>>>> inline: {query} <<<<<")
    result = re.match("[0-9]+[ ]?원", query)
    if result is not None:
        v = result.group().strip()
        inlines = []
        for n in money_names:
            r = google_money_exchange_rate(v, to=n)
            title = f"{r[0]} {r[2]}"
            text = f"{v} 는 {r[2]}로 {r[0]} 입니다."
            inlines.append(InlineQueryResultArticle(id=str(uuid4()), title=title, input_message_content=InputTextMessageContent(text)))
        await update.inline_query.answer(inlines)


application = Application.builder().token(TOKEN).build()
application.add_handler(InlineQueryHandler(inline_query))
application.run_polling(allowed_updates=Update.ALL_TYPES)
