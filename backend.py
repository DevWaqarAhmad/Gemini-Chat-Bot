import os
import uuid
import google.generativeai as genai
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langdetect import detect
from datetime import datetime

load_dotenv()
API_KEY = "AIzaSyDuBTqfrpAjTcJFh4kYVtIVAQvlEKMPyco"
if not API_KEY:
    raise ValueError("ERROR: GEMINI_API_KEY is missing! Set it in your .env file.")


genai.configure(api_key=API_KEY)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
conversation_memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=conversation_memory)


SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "prompt": "Respond in English about Butt Karahi's menu, locations, and prices.", "greeting": "Hello! How can I help you today?"},
    "ur": {"name": "Urdu", "prompt": "Butt Karahi کے مینو، مقامات اور قیمتوں کے بارے میں اردو میں جواب دیں۔", "greeting": "ہیلو! آج میں آپ کی کس طرح مدد کر سکتا ہوں؟"},
    "ar": {"name": "Arabic", "prompt": "الرد بالعربية حول قائمة مطعم بط كراهي والمواقع والأسعار.", "greeting": "مرحبًا! كيف يمكنني مساعدتك اليوم؟"},
    "hi": {"name": "Hindi", "prompt": "मेनू, स्थानों और कीमतों के बारे में हिंदी में उत्तर दें।", "greeting": "नमस्ते! आज मैं आपकी कैसे मदद कर सकता हूँ?"},
    "es": {"name": "Spanish", "prompt": "Responde en español sobre el menú, ubicaciones y precios de Butt Karahi.", "greeting": "¡Hola! ¿Cómo puedo ayudarte hoy?"},
    "fr": {"name": "French", "prompt": "Répondez en français sur le menu, les emplacements et les prix de Butt Karahi.", "greeting": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"},
    "zh-cn": {"name": "Chinese", "prompt": "用中文回答有关Butt Karahi的菜单、位置和价格。", "greeting": "你好！今天有什么可以帮您的吗？"},
    "bn": {"name": "Bengali", "prompt": "Butt Karahi-এর মেনু, অবস্থান এবং মূল্য সম্পর্কে বাংলায় উত্তর দিন।", "greeting": "হ্যালো! আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?"},
    "pa": {"name": "Punjabi", "prompt": "Butt Karahi ਦੇ ਮੀਨੂ, ਟਿਕਾਣਿਆਂ ਅਤੇ ਕੀਮਤਾਂ ਬਾਰੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।", "greeting": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡੀ ਆਜ਼ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ؟"},
    "tr": {"name": "Turkish", "prompt": "Butt Karahi'nin menüsü, konumları ve fiyatları hakkında Türkçe yanıt verin.", "greeting": "Merhaba! Bugün size nasıl yardımcı olabilirim?"}
}

MAX_HISTORY = 10  

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"

def GenerateResponse(input_text: str, previous_messages: list = None) -> str:
    try:
        user_lang = detect_language(input_text)
        lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])
        
        messages = [
            "System: " + lang_config["prompt"],
            "input: Who are you?",
            "output: I am an AI agent of Butt Karahi. I will help you choose the best menu item for you.",
            "input: Introduction",
            "output: Authentic Pakistani Cuisine\nHALAL | FRESH MEAT | DELICIOUS\nAt Butt Karahi, we believe in creating memories through food.",
            "input: Location",
            "output: Mississauga: 3015 Winston Churchill Blvd, ON L5L 2V8, Canada\nPickering: 820 Kingston Rd, ON L1V 1A8, Canada",
            "input: Featured Dishes / Special Dishes Menu",
            "output: Chicken Karahi\nVeal Karahi\nGoat Karahi\nPaneer Karahi\nDaal",
            "input: Appetizers Menu or Starter Menu",
            "output: Lahori Fried Fish – Spiced, crispy fried fish. CAD 21.99\nChanna Chaat – Chickpeas, potatoes, tomatoes, green chilies. CAD 9.99",
            "input: Karahi Specials",
            "output: Chicken Karahi – Charsi-style, salt & black pepper. (CAD 45.99)\nVeal Karahi – Specially flavored veal. (CAD 52.99)",
            "input: Other Categories",
            "output: Bar B.Q, Rice Creations, Vegetarian, Seafood, Naan & Breads, Desserts & Beverages.",
            "input: About us",
            "output: Established in 1979 in Lahore, Butt Karahi is known for its authentic taste, 100% halal meat, and hand-picked spices.",
            "input: Timing and Contact Number",
            "output: Mississauga Branch: +1 416-494-5477 | Pickering Branch: +1 905-839-0002",
        ]

        if previous_messages:
            for exchange in previous_messages:
                messages.append(f"input: {exchange['user']}")
                messages.append(f"output: {exchange['bot']}")

        messages.append(f"input: {input_text}")
        messages.append("output: ")

        response = model.generate_content(messages)
        return response.text
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

app = Flask(__name__)
CORS(app)

user_conversations = {}

@app.route("/")
def home():
    return "Flask Server is Running! Access the chatbot at /chat"

@app.route("/chat", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        # Get user_id from cookie or generate new
        user_id = request.cookies.get("user_id")
        new_user = False
        if not user_id:
            user_id = str(uuid.uuid4())
            new_user = True

        if not user_message:
            return jsonify({"error": "Please provide a valid input message."}), 400

        # Initialize history
        if user_id not in user_conversations:
            user_conversations[user_id] = []

        # Prepare history for input
        previous_messages = []
        for exchange in user_conversations[user_id]:
            msgs = exchange["messages"]
            previous_messages.append({
                "user": msgs[0]["text"],
                "bot": msgs[1]["text"]
            })

        # Generate bot response with history
        bot_response = GenerateResponse(user_message, previous_messages)

        # Append to history
        user_conversations[user_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "messages": [
                {"role": "user", "text": user_message},
                {"role": "bot", "text": bot_response}
            ]
        })

        # Limit history
        if len(user_conversations[user_id]) > MAX_HISTORY:
            user_conversations[user_id] = user_conversations[user_id][-MAX_HISTORY:]

        chat_history = user_conversations[user_id]

        # Send response with cookie if new user
        response = make_response(jsonify({"response": bot_response, "history": chat_history}))
        if new_user:
            response.set_cookie("user_id", user_id, httponly=True, samesite='Lax')

        return response

    except Exception as e:
        return jsonify({"error": f"Server Error: {str(e)}"}), 500

@app.route("/test", methods=["GET"])
def test():
    sample_input = request.args.get("q", "Tell me about your menu")
    return jsonify({"input": sample_input, "output": GenerateResponse(sample_input)})

if __name__ == '__main__':
    app.run(debug=True)
