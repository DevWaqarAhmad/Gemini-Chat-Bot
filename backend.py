import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
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

def GenerateResponse(input_text):
    response = model.generate_content([
  "input: Who are you",
  "output: i am AI Agent of Butt Karahi. how may i assist you?",
  "input: Introduction",
  "output: Butt Karahi Canada is a renowned Pakistani restaurant known for authentic Punjabi flavors and quality.\n\nExperience Punjabi cuisine at Butt Karahi. Enjoy dishes celebrating tradition and rich flavors.",
  "input: Address or Location",
  "output: Mississauga: 3015 Winston Churchill Blvd, ON L5L 2V8, Canada\nPickering: 820 Kingston Rd, ON L1V 1A8, Canada",
  "input: Featured or special dishes or signature dishes",
  "output: Chicken Karahi\nVeal Karahi\nGoat Karahi\nPaneer Karahi\nDaal",
  "input: Appetizers",
  "output: Lahori Fried Fish Spiced, crispy fried fish.\nChanna Chaat  Chickpeas, potatoes, tomatoes, green chilies.\nFresh Vegetable Salad  Cucumber, tomato, onion, lettuce.\nOnion Salad  Diced onions, green chilies, lemon.",
  "input: Karahi Specials:",
  "output: Chicken Karahi  Charsi-style, salt & black pepper. (CAD 45.99)\nVeal Karahi  Specially flavored veal. (CAD 52.99)\nGoat Karahi  Charsi-style goat meat. (CAD 75.99)\nLamb Karahi  Lamb with unique spices. (CAD 69.99)\nPaneer Karahi  Paneer in aromatic Karahi Masala. (CAD 24.99)\nDaal Channa  Chickpeas & lentils with butter. (CAD 11.99)",
  "input: Others categories",
  "output: Bar B.Q  Details not provided.\nRice Creations  Details not provided.\nVegetarian Daal Channa available.\nSeafood  Details not provided.\nNaan & Breads  Details not provided.\nDesserts & Beverages  Details not provided.",
  "input: about us",
  "output: Established in 1979 in Lahore, Butt Karahi is known for authentic taste, 100% halal meat, and hand-picked spices.",
  "input: All contact details of butt karahi",
  "output: Mississauga Branch:\n📍 3015 Winston Churchill Blvd, Mississauga, ON\n📞 +1 416-494-5477\n🕒 Mon: 3 PM-11 PM | Tue-Thu: 12 PM-11 PM | Fri-Sat: 12 PM-12 AM | Sun: 12 PM-11 PM\n\nPickering Branch:\n📍 820 Kingston Rd, Pickering, ON\n📞 +1 905-839-0002\n🕒 Same hours as Mississauga branch",
  f"input: {input_text}",
  "output: ",
])
    return response.text

#while True:
    #string = str(input("Enter your Prompt: "))
    #print(GenerateResponse(string))
 