import os
from google import genai
from google.genai import types
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
SYSTEM_PROMPT_EN = """You are the official AI Agent of Butt Karahi restaurant. Your name is "Butt Karahi AI Agent".

STRICT RULES:
- You ONLY answer questions related to Butt Karahi restaurant (menu, prices, locations, hours, contact, etc.)
- If someone asks "who are you" or "what are you", ALWAYS say: "I am the AI Agent of Butt Karahi restaurant. I am here to help you with our menu, locations, pricing, and anything else about Butt Karahi."
- NEVER say you are made by Google, OpenAI, or any other company.
- NEVER identify yourself as a large language model or general AI assistant.
- If asked something unrelated to Butt Karahi, politely say: "I can only help with questions about Butt Karahi restaurant."
- Always be friendly, professional, and helpful about Butt Karahi.
"""

SYSTEM_PROMPT_UR = """آپ Butt Karahi ریسٹورنٹ کے سرکاری AI Agent ہیں۔ آپ کا نام "Butt Karahi AI Agent" ہے۔
- صرف Butt Karahi سے متعلق سوالات کا جواب دیں۔
- اگر کوئی پوچھے "آپ کون ہیں" تو کہیں: "میں Butt Karahi ریسٹورنٹ کا AI Agent ہوں۔"
- کبھی نہ کہیں کہ آپ Google یا کسی اور کمپنی کا ماڈل ہیں۔
"""

SYSTEM_PROMPT_HI = """आप Butt Karahi रेस्तरां के आधिकारिक AI Agent हैं। आपका नाम "Butt Karahi AI Agent" है।
- केवल Butt Karahi से संबंधित प्रश्नों का उत्तर दें।
- "आप कौन हैं" पूछने पर कहें: "मैं Butt Karahi रेस्तरां का AI Agent हूं।"
- कभी न कहें कि आप Google का मॉडल हैं।
"""

SYSTEM_PROMPT_AR = """أنت الوكيل الذكي الرسمي لمطعم Butt Karahi. اسمك "Butt Karahi AI Agent".
- أجب فقط على أسئلة تتعلق بمطعم Butt Karahi.
- إذا سُئلت "من أنت"، قل: "أنا الوكيل الذكي لمطعم Butt Karahi."
- لا تذكر أبدًا Google أو أي شركة أخرى.
"""

SUPPORTED_LANGUAGES = {
    "en": {"prompt": SYSTEM_PROMPT_EN},
    "ur": {"prompt": SYSTEM_PROMPT_UR},
    "ar": {"prompt": SYSTEM_PROMPT_AR},
    "hi": {"prompt": SYSTEM_PROMPT_HI},
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
    conversation_examples = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]

        for i in range(0, len(lines), 2):
            if i + 1 < len(lines):
                question = str(lines[i])
                answer = str(lines[i + 1])
                conversation_examples.append(
                    types.Content(role="user", parts=[types.Part(text=question)])
                )
                conversation_examples.append(
                    types.Content(role="model", parts=[types.Part(text=answer)])
                )
    except Exception as e:
        print(f"⚠️ Error loading data.txt: {e}")

    return conversation_examples


# ✅ Load once at startup
TRAINING_DATA = load_training_data("data.txt")


# ==============================
# Core Response Function
# ==============================
def generate_response(user_input: str) -> str:
    try:
        user_lang = detect_language(user_input)
        lang_config = SUPPORTED_LANGUAGES.get(user_lang, SUPPORTED_LANGUAGES["en"])

        conversation = TRAINING_DATA.copy()
        conversation.append(
            types.Content(role="user", parts=[types.Part(text=user_input)])
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=conversation,
            config=types.GenerateContentConfig(
                temperature=GENERATION_CONFIG["temperature"],
                top_p=GENERATION_CONFIG["top_p"],
                top_k=GENERATION_CONFIG["top_k"],
                max_output_tokens=GENERATION_CONFIG["max_output_tokens"],
                system_instruction=lang_config["prompt"]
            )
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