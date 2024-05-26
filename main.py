import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import api_token, json_db, fun_generator, image_generator
import random, os
db = json_db.DatabaseInteraction()
fungen = fun_generator.FunGenerator()
imggen = image_generator.chooseRandomImage
commands = ["!gen", "!genimg"]
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот, который генерирует смешные тексты.")
    db.generate_chat_profile(str(update.effective_chat.id), 0, [])

async def message_listen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_chat_id = str(update.effective_chat.id)
    message_text = str(update.message.text)
    if message_text.lower() not in commands:
        db.add_text_data(message_chat_id, message_text)
    else:
        pass
    if (random.randint(1, 100) <= 20) or message_text.lower() in commands:
        if (random.randint(1, 100) <= 30) or message_text.lower() == "!genimg":
            print('hmm.. maybe you very lucky')
            message_chat_id = str(update.effective_chat.id)
            chat_words_count = int(db.get_chat_message_count(message_chat_id))
            chat_words = db.get_chat_messages(message_chat_id)
            if chat_words_count < 10:
                print('nah.. need more words')
            else:
                print('wow.. fun starts here')
                funny_text = fungen.generate(chat_words)
                await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("images/rnd_img/" + imggen("images/rnd_img"), 'rb'), caption=funny_text)
        else:
            print('hmm.. maybe you lucky')
            message_chat_id = str(update.effective_chat.id)
            chat_words_count = int(db.get_chat_message_count(message_chat_id))
            chat_words = db.get_chat_messages(message_chat_id)
            if chat_words_count < 10:
                print('nah.. need more words')
            else:
                print('wow.. fun starts here')
                funny_text = fungen.generate(chat_words)
                await context.bot.send_message(chat_id=update.effective_chat.id, text=funny_text)
    else:
        print('nah.. not now')

# async def generate_funny_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print('hmm.. maybe you lucky')
#     message_chat_id = str(update.effective_chat.id)
#     chat_words_count = int(db.get_chat_message_count(message_chat_id))
#     chat_words = db.get_chat_messages(message_chat_id)
#     if chat_words_count < 10:
#         print('nah.. need more words')
#     else:
#         print('wow.. fun starts here')
#         funny_text = fungen.generate(chat_words)
#         wait context.bot.send_message(chat_id=update.effective_chat.id, text=funny_text)
#     else:
#         print('nah.. not now')


if __name__ == '__main__':
    application = ApplicationBuilder().token(api_token.apitoken).build()

    messsage_listener_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), message_listen)
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(messsage_listener_handler)
    
    application.run_polling()