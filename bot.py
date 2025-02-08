import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔥 Step 1: Text Files Load कर
def load_text_files(folder_path):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                docs.append(f.read())
    return docs

data_folder = "data"  # Apni files "data" folder me daal
documents = load_text_files(data_folder)

# 🔥 Step 2: AI Model (Text Understanding)
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents, convert_to_numpy=True)

# 🔥 Step 3: FAISS Fast Search Engine
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# 🔥 Step 4: Query Search Function
def search_query(query, top_k=1):
    query_embedding = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_embedding, top_k)
    results = [documents[i] for i in indices[0]]
    return results if results else ["❌ Bhai, iska jawab nahi mila!"]

# 🔥 Step 5: Telegram Bot Setup
BOT_TOKEN = "7365299503:AAGqaBqSHS5fePkJ1g7B3bqyo32I8ZP_eho"

def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 Bhai, koi bhi hacking / pentesting ka sawaal pooch!")

def handle_message(update: Update, context: CallbackContext):
    user_query = update.message.text
    answers = search_query(user_query, top_k=1)
    response = f"🔹 {answers[0][:500]}..." if answers else "❌ Bhai, iska jawab nahi mila!"
    update.message.reply_text(response)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    print("📡 Telegram Bot Ready! Chal gaya bhai... 🚀")
    main()