import requests

BOT_TOKEN = "8701758526:AAFHAp2AF4jaYpxUkyhAo0nqPKGpzQVI650"
GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

SYSTEM_PROMPT = """تو یه دستیار هوش مصنوعی فارسی هستی.
- همیشه به فارسی جواب بده
- مودب و حرفه ای باش
- به هر سوالی جواب بده
- در انتها بگو: برای محتوای بیشتر پیج ما رو دنبال کن 👉 @Kaveh6294"""

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def send_typing(chat_id):
    requests.post(f"{TELEGRAM_URL}/sendChatAction", json={"chat_id": chat_id, "action": "typing"})

def ask_groq(user_message):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama3-8b-8192", "messages": [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_message}], "max_tokens": 1000}
    response = requests.post(GROQ_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

def handle_update(update):
    if "message" not in update:
        return
    message = update["message"]
    chat_id = message["chat"]["id"]
    if "text" not in message:
        return
    text = message["text"]
    user_name = message["from"].get("first_name", "کاربر")
    if text == "/start":
        send_message(chat_id, f"سلام {user_name}! 👋\n\n🤖 به ربات هوش مصنوعی فارسی خوش اومدی!\n\nهر سوالی داری بپرس! 😊\n\n📱 @Kaveh6294")
        return
    send_typing(chat_id)
    try:
        response = ask_groq(text)
        send_message(chat_id, response)
    except:
        send_message(chat_id, "متاسفم مشکلی پیش اومد دوباره امتحان کن!")

def main():
    print("ربات شروع به کار کرد!")
    offset = 0
    while True:
        try:
            response = requests.get(f"{TELEGRAM_URL}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
            updates = response.json().get("result", [])
            for update in updates:
                handle_update(update)
                offset = update["update_id"] + 1
        except Exception as e:
            print(f"خطا: {e}")

if __name__ == "__main__":
    main()
