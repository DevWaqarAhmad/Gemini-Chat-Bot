# import os
# import hmac
# import hashlib
# from google import genai
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from dotenv import load_dotenv
# from langchain_google_genai import GoogleGenerativeAI
# from langchain.chains import ConversationChain
# from langchain.memory import ConversationBufferMemory
# from langdetect import detect

# # Initialize Flask App
# app = Flask(__name__)
# CORS(app)

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError("ERROR: GEMINI_API_KEY is missing! Set it in your environment.")

# # # Gemini Model Configuration
# # genai.configure(api_key=API_KEY)
# # generation_config = {
# #     "temperature": 1,
# #     "top_p": 0.95,
# #     "top_k": 40,
# #     "max_output_tokens": 8192,
# #     "response_mime_type": "text/plain",
# # }
# # model = genai.GenerativeModel(
# #     model_name="gemini-2.5-flash",
# #     generation_config=generation_config,
# # )


# # ✅ NEW Gemini Client Initialization
# client = genai.Client(api_key=API_KEY)

# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 40,
#     "max_output_tokens": 8192,
# }

# # LangChain Setup
# llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=API_KEY)
# memory = ConversationBufferMemory()
# conversation = ConversationChain(llm=llm, memory=memory)

# # Supported Languages
# SUPPORTED_LANGUAGES = {
#     "en": {"name": "English", "prompt": "Respond in English about Butt Karahi's menu, locations, and prices.", "greeting": "Hello! How can I help you today?"},
#     "ur": {"name": "Urdu", "prompt": "Butt Karahi کے مینو، مقامات اور قیمتوں کے بارے میں اردو میں جواب دیں۔", "greeting": "ہیلو! آج میں آپ کی کس طرح مدد کر سکتا ہوں؟"},
#     "ar": {"name": "Arabic", "prompt": "الرد بالعربية حول قائمة مطعم بط كراهي والمواقع والأسعار.", "greeting": "مرحبًا! كيف يمكنني مساعدتك اليوم؟"},
#     "hi": {"name": "Hindi", "prompt": "मेनू, स्थानों और कीमतों के बारे में हिंदी में उत्तर दें।", "greeting": "नमस्ते! आज मैं आपकी कैसे मदद कर सकता हूँ?"},
#     "es": {"name": "Spanish", "prompt": "Responde en español sobre el menú, ubicaciones y precios de Butt Karahi.", "greeting": "¡Hola! ¿Cómo puedo ayudarte hoy?"},
#     "fr": {"name": "French", "prompt": "Répondez en français sur le menu, les emplacements et les prix de Butt Karahi.", "greeting": "Bonjour ! Comment puis-je vous aider aujourd'hui ?"},
#     "zh-cn": {"name": "Chinese", "prompt": "用中文回答有关Butt Karahi的菜单、位置和价格。", "greeting": "你好！今天有什么可以帮您的吗？"},
#     "bn": {"name": "Bengali", "prompt": "Butt Karahi-এর মেনু, অবস্থান এবং মূল্য সম্পর্কে বাংলায় উত্তর দিন।", "greeting": "হ্যালো! আজ আমি আপনাকে কিভাবে সাহায্য করতে পারি?"},
#     "pa": {"name": "Punjabi", "prompt": "Butt Karahi ਦੇ ਮੀਨੂ, ਟਿਕਾਣਿਆਂ ਅਤੇ ਕੀਮਤਾਂ ਬਾਰੇ ਪੰਜਾਬੀ ਵਿੱਚ ਜਵਾਬ ਦਿਓ।", "greeting": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡੀ ਆਜ਼ ਕਿਵੇਂ ਮਦਦ ਕਰ ਸਕਦਾ ਹਾਂ؟"},
#     "tr": {"name": "Turkish", "prompt": "Butt Karahi'nin menüsü, konumları ve fiyatları hakkında Türkçe yanıt verin.", "greeting": "Merhaba! Bugün size nasıl yardımcı olabilirim?"}
# }

# # Helper Functions
# def detect_language(text: str) -> str:
#     try:
#         lang = detect(text)
#         return lang if lang in SUPPORTED_LANGUAGES else "en"
#     except Exception:
#         return "en"


# # def generate_response(input_text: str, language: str, context: str = "") -> str:
# #     try:
# #         # Language detection
# #         if language == "Auto-Detect":
# #             user_lang = detect_language(input_text)
# #         else:
# #             user_lang = language
        
# #         lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

# #         # Build structured conversation examples (your training queries)
# #         conversation_examples = [
# #             {"role": "user", "parts": ["Who are you?"]},
# #             {"role": "model", "parts": ["I am an AI agent of Butt Karahi. I will help you choose the best menu item for you."]},

# #             {"role": "user", "parts": ["Introduction"]},
# #             {"role": "model", "parts": ["Authentic Pakistani Cuisine\nHALAL | FRESH MEAT | DELICIOUS\nAt Butt Karahi, we believe in creating memories through food."]},

# #             {"role": "user", "parts": ["Location"]},
# #             {"role": "model", "parts": ["Mississauga: 3015 Winston Churchill Blvd, ON L5L 2V8, Canada\nPickering: 820 Kingston Rd, ON L1V 1A8, Canada"]},

# #             {"role": "user", "parts": ["Featured Dishes / Special Dishes Menu"]},
# #             {"role": "model", "parts": ["Chicken Karahi\nVeal Karahi\nGoat Karahi\nPaneer Karahi\nDaal"]},

# #             {"role": "user", "parts": ["kids menu"]},
# #             {"role": "model", "parts": ["VILLAGE FRIES CAD 6.99 | CRISPY GARLIC FRIES CAD 7.99 | CHICKEN CHEESE BALLS WITH FRIES (5 PIECES) CAD 9.99 | TIKKA BOTI ROLL CAD 11.99 | KABAB ROLL CAD 11.99"]},

# #             # 👉 Yahan aap apni baki menu categories bhi isi format me add kar sakte hain
# #         ]

# #         # Final user input
# #         conversation_examples.append(
# #             {"role": "user", "parts": [f"{context}\n{input_text}"]}
# #         )

# #         response = client.models.generate_content(
# #             model="gemini-2.5-flash",
# #             contents=conversation_examples,
# #             config={
# #                 "temperature": 1,
# #                 "top_p": 0.95,
# #                 "top_k": 40,
# #                 "max_output_tokens": 8192,
# #                 "system_instruction": lang_config["prompt"]
# #             }
# #         )

# #         return response.text

# #     except Exception as e:
# #         return f"❌ ERROR: {str(e)}"


# def generate_response(input_text: str, language: str, context: str = "") -> str:
#     try:
#         if language == "Auto-Detect":
#             user_lang = detect_language(input_text)
#         else:
#             user_lang = language
        
#         lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

#         # Load training examples from file
#         conversation_examples = load_training_data("data.txt")

#         # Add current user query
#         conversation_examples.append(
#             {"role": "user", "parts": [f"{context}\n{input_text}"]}
#         )

#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=conversation_examples,
#             config={
#                 "temperature": 1,
#                 "top_p": 0.95,
#                 "top_k": 40,
#                 "max_output_tokens": 8192,
#                 "system_instruction": lang_config["prompt"]
#             }
#         )

#         return response.text

#     except Exception as e:
#         return f"❌ ERROR: {str(e)}"

# # API Routes
# @app.route('/chat', methods=['POST'])
# def chat():
#     # Get user input directly from the request body
#     user_input = request.form.get('message')  # Getting message from the frontend form
    
#     if not user_input:
#         return jsonify({'error': 'No message provided.'}), 400

#     # Detect language of the input
#     user_lang = detect_language(user_input)
#     lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

#     system_prompt = lang_config["prompt"]

#     # Generate response using LangChain's conversation memory
#     full_input = f"{system_prompt}\nUser: {user_input}"
#     bot_response = conversation.run(full_input)

#     return jsonify({'response': bot_response})

# @app.route('/', methods=['GET'])
# def home():
#     return "Chatbot is running!"



# if __name__ == '__main__':
#     app.run(debug=True)



import os
from google import genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langdetect import detect

# ==============================
# Flask Initialization
# ==============================
app = Flask(__name__)
CORS(app)

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY is missing in environment variables.")

# ==============================
# Gemini Client Initialization
# ==============================
client = genai.Client(api_key=API_KEY)

GENERATION_CONFIG = {
    "temperature": 0.8,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# ==============================
# Supported Languages
# ==============================
SUPPORTED_LANGUAGES = {
    "en": {
        "prompt": "Respond professionally in English about Butt Karahi's menu, locations, prices and restaurant details."
    },
    "ur": {
        "prompt": "Butt Karahi کے مینو، مقامات اور قیمتوں کے بارے میں اردو میں پیشہ ورانہ انداز میں جواب دیں۔"
    },
    "ar": {
        "prompt": "الرد باللغة العربية بشكل احترافي حول قائمة مطعم بط كراهي والمواقع والأسعار."
    },
    "hi": {
        "prompt": "मेनू, स्थानों और कीमतों के बारे में हिंदी में पेशेवर तरीके से उत्तर दें।"
    }
}

# ==============================
# Helper Functions
# ==============================
def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang if lang in SUPPORTED_LANGUAGES else "en"
    except:
        return "en"


def load_training_data(file_path="data.txt"):
    """
    Expected format in data.txt:
    Question line
    Answer line
    (blank line optional)
    """
    conversation_examples = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                question = lines[i]
                answer = lines[i + 1]

                conversation_examples.append({
                    "role": "user",
                    "parts": [question]
                })

                conversation_examples.append({
                    "role": "model",
                    "parts": [answer]
                })

    except Exception as e:
        print(f"⚠️ Error loading data.txt: {e}")

    return conversation_examples


# ✅ Load once at startup (efficient)
TRAINING_DATA = load_training_data("data.txt")


# ==============================
# Core Response Function
# ==============================
def generate_response(user_input: str) -> str:
    try:
        user_lang = detect_language(user_input)
        lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

        # Copy training data so original remains unchanged
        conversation = TRAINING_DATA.copy()

        # Add user query at end
        conversation.append({
            "role": "user",
            "parts": [user_input]
        })

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation,
            config={
                **GENERATION_CONFIG,
                "system_instruction": lang_config["prompt"]
            }
        )

        return response.text

    except Exception as e:
        return f"❌ ERROR: {str(e)}"


# ==============================
# API Routes
# ==============================
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form.get('message')

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    bot_response = generate_response(user_input)

    return jsonify({'response': bot_response})


@app.route('/', methods=['GET'])
def home():
    return "✅ Butt Karahi AI Chatbot is running."


# ==============================
# Run Server
# ==============================
if __name__ == '__main__':
    app.run(debug=True)