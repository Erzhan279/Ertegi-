import os
import telebot
import requests

# 🔒 Құпия параметрлер (Render environment variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
OWNER_ID = int(os.getenv("OWNER_ID"))  # Сенің Telegram ID-ң

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_story():
    prompt = (
        "6-10 жастағы балаларға арналған өте қызықты, күлкілі, тәрбиелік мәні бар қысқа ертегі жаз. "
        "Ертегіге көңілді кейіпкерлер қос (жануарлар, сиқыршы, бала немесе ғажайып достар). "
        "Әңгіме 5-7 сөйлемнен аспасын. "
        "Бастапқы жолда әдемі атауын жаз, мысалы: 🌟 «Күлкілі Түлкі мен Айдаһар» 🌟\n\n"
        "Сосын негізгі мәтінді жаз. Эмодзилерді көбірек пайдалан (мысалы: 🦊🐰🐉🌈✨😂❤️). "
        "Соңында бір сөйлемдік жақсы мораль немесе қорытынды болсын.\n\n"
        "Мәтінді балаларға түсінікті, көңілді, жылы және әдемі стильде жаз."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    response = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]})
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Ертегіні алу кезінде қате болды: {e}"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Сәлем 👋 Мен балаларға арналған ертегі ботпын! ✨\n"
        "Мен арнаға күн сайын күлкілі, қызықты, сиқырлы ертегілер жариялап отырам 🌈\n\n"
        "Егер сен админ болсаң — /gostart деп жазып, бірден 3 жаңа ертегі жарияла!"
    )

@bot.message_handler(commands=['gostart'])
def gostart(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "⛔ Бұл команданы тек бот иесі қолдана алады.")
        return

    bot.send_message(message.chat.id, "🌟 3 жаңа ертегі дайындалып жатыр... күте тұр ⏳")

    for i in range(1, 4):
        try:
            story = generate_story()
            text = f"📖 *Ертегі #{i}:*\n\n{story}"
            bot.send_message(CHANNEL_USERNAME, text, parse_mode="Markdown")
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ {i}-ертегіні шығару кезінде қате болды: {e}")

    bot.send_message(message.chat.id, "✅ 3 ертегі каналға сәтті жарияланды!")

print("🤖 Бот іске қосылды...")
bot.polling(none_stop=True)
