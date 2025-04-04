from datetime import datetime
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://devwaqarahmad:nKuui_t2WMiKtpe@cluster0.fegz8dj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["chatbot_db"]
conversations_collection = db["conversations"]

def save_chat_to_db(user_id, user_input, bot_response):
    """Save the conversation between the user and the bot."""
    conversations_collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "messages": [
            {"role": "user", "text": user_input},
            {"role": "bot", "text": bot_response}
        ]
    })

def get_chat_history(user_id):
    """Retrieve the chat history for a specific user."""
    chats = conversations_collection.find({"user_id": user_id}).sort("timestamp")
    history = []
    for chat in chats:
        history.extend(chat["messages"])
    return history
