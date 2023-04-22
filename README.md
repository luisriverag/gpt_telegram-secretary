A Telegram bot connected to ChatGPT API written in Python. Understands voice commands, and sends its replies both as text and voice attachments

Dev credit goes to GPT4, I just helped with a few prompts

You'll need to add your OpenAI and Telegram API keys, and probably install required libraries with

-pip install -r requirements.txt

Then just python3 bot.py

-----

To get an OpenAI API key:

Go to the OpenAI website at https://openai.com/

Click on the "API" link at the top of the page.

Click on the "Get started for free" button.

Fill out the registration form with your email address and a password.

Verify your email address by clicking on the link in the verification email that OpenAI sends you.

Once you're logged in, click on the "API keys" link at the top of the page.

Click on the "Create API key" button and follow the instructions to generate your API key.

-----

To create a new Telegram bot with BotFather:

Open the Telegram app on your device and search for "BotFather".

Tap on the "BotFather" chat to open it.

Type "/start" and send the message.

Follow the instructions that BotFather sends you to set up your new bot, including giving it a name and a username.

Once you have created your bot, BotFather will send you an API token. Keep this token safe, as it will be required to interact with your bot using the Telegram API.


----

To add them at the end of your bashrc

nano  ~/.bashrc

export TELEGRAM_API_KEY="<your_telegram_token>"
export OPENAI_API_KEY="<your_openai_api_key>"

