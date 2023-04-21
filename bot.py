import os
import logging
import telegram
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import requests

TELEGRAM_TOKEN = '<your_telegram_token>'
OPENAI_API_KEY = '<your_openai_api_key>'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user_conversations[user_id] = [{'role': 'system', 'content': 'You are chatting with an AI assistant.'}]
    update.message.reply_text('Hi! You are chatting with a bot from @luisriverag developed by GPT4. It uses GPT3.5 via API amongst others.')

def chatgpt_request(prompt, conversation_history):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }
    data = {
        'messages': conversation_history + [{'role': 'user', 'content': prompt}],
        'model': 'gpt-3.5-turbo'
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()

def chat(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    prompt = update.message.text

    if user_id not in user_conversations:
        user_conversations[user_id] = [{'role': 'system', 'content': 'You are chatting with an AI assistant.'}]

    response = chatgpt_request(prompt, user_conversations[user_id])
    user_conversations[user_id].append({'role': 'user', 'content': prompt})
    user_conversations[user_id].append({'role': 'assistant', 'content': response})
    
    update.message.reply_text(response)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(telegram.ext.Filters.text & ~telegram.ext.Filters.command, chat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
