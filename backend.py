import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langdetect import detect

#load_dotenv()
#API_KEY = os.getenv("GEMINI_API_KEY")
API_KEY = "AIzaSyDuBTqfrpAjTcJFh4kYVtIVAQvlEKMPyco"

if not API_KEY:
    raise ValueError("❌ ERROR: GEMINI_API_KEY is missing! Set it in your .env file.")

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
    "en": {
        "name": "English",
        "prompt": "Respond in English about Butt Karahi's menu, locations, and prices.",
        "greeting": "Hello! How can I help you today?"
    },
    "ur": {
        "name": "Urdu",
        "prompt": "Butt Karahi کے مینو، مقامات اور قیمتوں کے بارے میں اردو میں جواب دیں۔",
        "greeting": "ہیلو! آج میں آپ کی کس طرح مدد کر سکتا ہوں؟"
    },
    "ar": {
        "name": "Arabic",
        "prompt": "الرد بالعربية حول قائمة مطعم بط كراهي والمواقع والأسعار.",
        "greeting": "مرحبًا! كيف يمكنني مساعدتك اليوم؟"
    },
    "hi": {
        "name": "Hindi",
        "prompt": "मेनू, स्थानों और कीमतों के बारे में हिंदी में उत्तर दें।",
        "greeting": "नमस्ते! आज मैं आपकी कैसे मदद कर सकता हूँ?"
    },
    "es": {
        "name": "Spanish",
        "prompt": "Responde en español sobre el menú, ubicaciones y precios de Butt Karahi.",
        "greeting": "¡Hola! ¿Cómo puedo ayudarte hoy?"
    },
    "fr": {
        "name": "French",
        "prompt": "Répondez en français sur le menu, les emplacements et les prix de Butt Karahi.",
        "greeting": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    },
    "zh-cn": {
        "name": "Chinese",
        "prompt": "用中文回答有关Butt Karahi的菜单、位置和价格。",
        "greeting": "你好！今天有什么可以帮您的吗？"
    },
    "bn": {
        "name": "Bengali",
        "prompt": "Butt Karahi-এর মেনু, অবস্থান এবং মূল্য সম্পর্কে বাংলায় উত্তর দিন।",
        "greeting": "হ্যালো! আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?"
    },
    "pa": {
        "name": "Punjabi",
        "prompt": "Butt Karahi ਦੇ ਮੀਨੂ, ਟਿਕਾਣਿਆਂ ਅਤੇ ਕੀਮਤਾਂ ਬਾਰੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।",
        "greeting": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡੀ ਆਜ਼ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ?"
    },
    "tr": {
        "name": "Turkish",
        "prompt": "Butt Karahi'nin menüsü, konumları ve fiyatları hakkında Türkçe yanıt verin.",
        "greeting": "Merhaba! Bugün size nasıl yardımcı olabilirim?"
    }
}

def detect_language(text: str) -> str:
    """Detects language and falls back to English if unsupported."""
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"

def GenerateResponse(input_text: str) -> str:
    """Generates a multilingual response based on user input."""
    try:
        user_lang = detect_language(input_text)
        lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])
        
        response = model.generate_content([
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
            f"input: {input_text}",
            "output: ",
        ])
        return response.text
    except Exception as e:
        return f"❌ ERROR: {str(e)}"

app = Flask(__name__)
CORS(app)  

@app.route("/")
def home():
    return "Flask Server is Running! Access the chatbot at /chat"

@app.route('/chat', methods=['POST'])
def chatbot():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": " Please provide a valid input message."}), 400

        bot_response = GenerateResponse(user_message)
        return jsonify({"response": bot_response})
    
    except Exception as e:
        return jsonify({"error": f" Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)