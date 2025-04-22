import os
import hmac
import hashlib
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langdetect import detect

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Load Environment Variables (Optional if you use .env)
# load_dotenv()

# API Key for Google Generative AI
API_KEY = "AIzaSyDuBTqfrpAjTcJFh4kYVtIVAQvlEKMPyco"

if not API_KEY:
    raise ValueError("ERROR: GEMINI_API_KEY is missing! Set it in your environment.")

# Gemini Model Configuration
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
# Set up LangChain LLM and Memory
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Supported Languages
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

# Helper Functions
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except Exception:
        return "en"
def generate_response(input_text: str, language: str, context: str = "") -> str:
    try:
        # Detect the language if it's not passed as argument
        if language == "Auto-Detect":
            user_lang = detect_language(input_text)
        else:
            user_lang = language
        
        lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

        # Construct the full prompt by combining the context and the input text
        full_prompt = f"{context}\ninput: {input_text}\noutput:"

        # Generate response using the model with memory
        response = model.generate_content([  # Assuming you're using the generative model here
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
            "input: kids menu",
            "output: VILLAGE FRIES CAD 6.99 | CRISPY GARLIC FRIES CAD 7.99 | CHICKEN CHEESE BALLS WITH FRIES (5 PIECES) CAD 9.99 | TIKKA BOTI ROLL CAD 11.99 | KABAB ROLL CAD 11.99",
            "input: karahi menu",
            "output: BUTT SPECIAL GOAT KARAHI Half: CAD 44.99 / Full: CAD 75.99 | CHARSI GOAT KARAHI Half: CAD 44.99 / Full: CAD 75.99 | BUTT SPECIAL LAMB KARAHI Half: CAD 39.99 / Full: CAD 69.99 | CHARSI LAMB KARAHI Half: CAD 39.99 / Full: CAD 69.99 | BUTT SPECIAL VEAL KARAHI Half: CAD 33.99 / Full: CAD 52.99 | VEAL CHARSI KARAHI Half: CAD 33.99 / Full: CAD 52.99 | BUTT SPECIAL CHICKEN KARAHI (BONE-IN) Half: CAD 29.99 / Full: CAD 45.99 | BUTT SPECIAL CHICKEN KARAHI (BONELESS) Half: CAD 32.99 / Full: CAD 50.99 | CHICKEN WHITE KARAHI (BONE-IN) Half: CAD 29.99 / Full: CAD 45.99 | CHICKEN WHITE KARAHI (BONELESS) Half: CAD 32.99 / Full: CAD 50.99 | CHARSI CHICKEN KARAHI (BONE-IN) Half: CAD 29.99 / Full: CAD 45.99 | MAKHMALI CHICKEN KARAHI Half: CAD 29.99 / Full: CAD 45.99 | MALAI TIKKA KARAHI Full: CAD 30.99 | CHICKEN / BEEF KABAB KARAHI Full: CAD 31.99 | DAAL GOSHT (VEAL OR GOAT) CAD 30.99",
            "input: barbq menu",
            "output: CHICKEN SEEKH KEBAB (3 PIECES) CAD 17.99 | CHICKEN TIKKA BOTI (5 PIECES) CAD 17.99 | CHICKEN MALAI BOTI (5 PIECES) CAD 19.99 | BEEF SEEKH KEBAB (3 PIECES) CAD 18.99 | PANEER TIKKA (3 PIECES) CAD 15.99 | RAITA (ADD-ONS) CAD 2.99 | MINT RAITA (ADD-ONS) CAD 2.99 | KHATTI MEETHI CHATNI (ADD-ONS) CAD 2.99",
            "input: Rice Menu",
            "output: CHICKEN BIRYANI CAD 17.99 | CHICKEN TIKKA BIRYANI CAD 17.99 | YAKHNI PULAO CAD 19.99 | MATAR PULAO CAD 12.99 | NEW YORK STYLE GYRO CAD 17.99 | DELICIOUS TIKKA ON THE RICE CAD 17.99 | SIZZLING KEBAB ON THE RICE CAD 17.99 | CRISPY FISH ON THE RICE CAD 17.99 | WHITE RICE CAD 5.99",
            "input: vegetable menu",
            "output: PANEER KARAHI CAD 21.99 | DAAL CHANNA CAD 12.99 | KHOYE WALY CHANNY CAD 13.99 | VEGETABLE OF THE DAY CAD 13.99",
            "input: Sea Food Menu",
            "output: Fish Karahi CAD 24.99",
            "input: Naan & Bread Menu",
            "output: PLAIN NAAN CAD 2.99 | TANDOORI ROTI CAD 2.99 | KHAMEERI ROTI CAD 2.99 | KAIVANJI NAAN CAD 3.49 | BUTTER NAAN CAD 2.99 | SESAME NAAN (KULCHA) CAD 3.49 | GARLIC NAAN CAD 4.49",
            "input: Desserts Menu",
            "output: KHEER CAD 8.99 | GAJRELLA CAD 6.99 | GULAB JAMUN (2 PIECES) CAD 4.99 | ZARDA RICE (SWEET RICE) CAD 9.99 | ICE-CREAM CAD 4.99 | RABRI FALOODA CAD 11.99 | KHOYE WALI KULFI CAD 3.99",
            "input: Cold & Hot Drinks Menu",
            "output: MANGO LASSI CAD 6.99 | MANGO SHAKE CAD 6.99 | MINT MARGARITA CAD 7.99 | LASSI (SWEET/SALTY) CAD 4.99 | LASSI JUG (SWEET/SALTY) CAD 19.99 | LEMONADE CAD 4.99 | PAKOLA CAD 2.99 | PESHAWARI KAHWA CAD 2.99 | KARAK CHAI CAD 4.49 | POP CAD 2.49 | SPRING WATER Large CAD 3.49 / Small CAD 1.49",


            full_prompt
        ])

        return response.text
    except Exception as e:
        return f"❌ ERROR: {str(e)}"



# API Routes
@app.route('/chat', methods=['POST'])
def chat():
    # Get user input directly from the request body
    user_input = request.form.get('message')  # Getting message from the frontend form
    
    if not user_input:
        return jsonify({'error': 'No message provided.'}), 400

    # Detect language of the input
    user_lang = detect_language(user_input)
    lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

    system_prompt = lang_config["prompt"]

    # Generate response using LangChain's conversation memory
    full_input = f"{system_prompt}\nUser: {user_input}"
    bot_response = conversation.run(full_input)

    return jsonify({'response': bot_response})

@app.route('/', methods=['GET'])
def home():
    return "Chatbot is running!"



if __name__ == '__main__':
    app.run(debug=True)
