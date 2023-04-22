import os
import logging
import requests
import telegram
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import tempfile
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

user_conversations = {}

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat_id
    user_conversations[user_id] = [{'role': 'system', 'content': 'You are chatting with an AI assistant.'}]
    update.message.reply_text('Hi! You are chatting with a bot from @luisriverag developed by GPT4. It uses GPT3.5 via API amongst others.')

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_ogg(file_path)
    audio.export("temp.wav", format="wav")
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = None
    return text

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

    if update.message.voice:
        file = context.bot.getFile(update.message.voice.file_id)
        file.download("voice_note.oga")

        prompt = transcribe_audio("voice_note.oga")
        if prompt is None:
            update.message.reply_text("Sorry, I couldn't understand the voice note. Please try again.")
            return
    else:
        prompt = update.message.text

    if user_id not in user_conversations:
        user_conversations[user_id] = [{'role': 'system', 'content': 'You are chatting with an AI assistant.'}]

    response = chatgpt_request(prompt, user_conversations[user_id])
    user_conversations[user_id].append({'role': 'user', 'content': prompt})
    user_conversations[user_id].append({'role': 'assistant', 'content': response})
    
    update.message.reply_text(response)

    # Convert response to audio and send as a voice message
    tts = gTTS(text=response, lang='en')
    with tempfile.NamedTemporaryFile(mode="wb", suffix=".mp3", delete=False) as f:
        tts.save(f.name)
        f.flush()
        update.message.reply_voice(voice=open(f.name, 'rb'))
        os.unlink(f.name)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler((telegram.ext.Filters.text | telegram.ext.Filters.voice), chat))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
