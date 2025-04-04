import datetime
from pymongo import MongoClient

# Assuming you have a MongoDB connection
client = MongoClient("mongodb://localhost:27017")  # Replace with your actual MongoDB URI
db = client["chat_database"]  # Replace with your database name
conversations_collection = db["conversations"]  # Replace with your collection name

# Save chat history to the database with a specific user_id
def save_chat_to_db(user_id, user_input, bot_response):
    conversations_collection.insert_one({
        "user_id": user_id,
        "timestamp": datetime.datetime.utcnow(),
        "messages": [
            {"role": "user", "text": user_input},
            {"role": "bot", "text": bot_response}
        ]
    })

# Retrieve the chat history for a specific user_id
def get_chat_history(user_id):
    chats = conversations_collection.find({"user_id": user_id}).sort("timestamp")
    history = []
    for chat in chats:
        history.extend(chat["messages"])
    return history

# Example of how GenerateResponse can use the saved chat history
def GenerateResponse(user_input, user_id=None):
    # Optionally retrieve chat history for personalization
    chat_history = get_chat_history(user_id) if user_id else []

    # Your logic to generate a bot response
    bot_response = f"Bot response to: {user_input}"  # Replace with real response logic

    # Save conversation if user_id is provided
    if user_id:
        save_chat_to_db(user_id, user_input, bot_response)

    return bot_response
