import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key="AIzaSyBL-AxG9VvXh36fN1HidspNonA11DX4jgI")
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Function to generate chatbot response
def GenerateResponse(input_text):
    """Generates a response based on user input."""
    response = model.generate_content([
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

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/chat', methods=['POST'])
def chatbot():
    data = request.json
    user_message = data.get("message", "")

    # Get response from Gemini AI
    bot_response = GenerateResponse(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
