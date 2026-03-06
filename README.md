# Gemini AI Chatbot Agent

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Flask](https://img.shields.io/badge/Flask-API-black)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# Overview

**Gemini AI Chatbot Agent** is a conversational AI application built using **Google Gemini Generative AI**.
The system allows users to interact with an intelligent chatbot capable of understanding queries, detecting languages, and generating context-aware responses.

The application uses:

* **Streamlit** for the interactive web interface
* **Flask** for backend API services
* **Google Gemini API** for AI-powered responses

This project demonstrates how **Generative AI models can be integrated into real-time web applications to build intelligent AI agents.**

---

# Key Features

* AI chatbot powered by **Google Gemini API**
* Interactive **Streamlit chatbot interface**
* **Flask REST API** backend
* Automatic **language detection**
* Secure API key handling using **dotenv**
* Cross-origin request handling with **Flask-CORS**
* Modular and scalable backend structure
* Session handling using **UUID**

---

# Architecture

```
User
  │
  ▼
Streamlit Chat UI
  │
  ▼
Flask Backend API
  │
  ▼
Google Gemini API
  │
  ▼
AI Generated Response
  │
  ▼
Streamlit Chat Interface
```

The chatbot works through a **client-server architecture** where Streamlit sends requests to the Flask backend, which then communicates with the **Gemini AI model** to generate responses.

---

# Tech Stack

## Frontend

* Streamlit

## Backend

* Flask
* Python

## AI Model

* Google Gemini (Generative AI)

## Libraries

* streamlit
* flask
* flask-cors
* google-genai
* python-dotenv
* langdetect
* uuid

---

# Project Structure

```
gemini-ai-chatbot/
│
├── app.py
│   Streamlit chatbot interface
│
├── backend.py
│   Flask API handling chatbot requests
│
├── .env
│   Environment variables (API keys)
│
├── requirements.txt
│   Project dependencies
│
└── README.md
```

---

# Installation

## 1 Clone the repository

```
git clone https://github.com/yourusername/gemini-ai-chatbot.git
cd gemini-ai-chatbot
```

---

## 2 Create Virtual Environment

```
python -m venv venv
```

Activate environment

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

---

## 3 Install Dependencies

```
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file in the project root directory.

```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from **Google AI Studio**.

---

# Running the Application

## Start Flask Backend

```
python backend.py
```

---

## Start Streamlit Interface

```
streamlit run app.py
```

Open the URL provided by Streamlit in your browser.

---

# Example Code Snippet

```python
import streamlit as st
import uuid
import backend
import os
from google import genai
from google.genai import types
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langdetect import detect
```

---

# Use Cases

* AI virtual assistants
* Customer support chatbots
* Knowledge base assistants
* AI automation tools
* Educational AI applications

---

# Future Improvements

* Conversation memory
* Retrieval Augmented Generation (RAG)
* Voice-based chatbot
* Multi-agent AI systems
* Authentication system
* Cloud deployment (AWS / GCP)

---

# Security

* API keys should always be stored in `.env`
* Never push `.env` files to public repositories

---

# License

This project is licensed under the **MIT License**.

---

# Author

AI Chatbot Agent developed using **Google Gemini Generative AI**, demonstrating integration of **LLM APIs with web applications** using **Streamlit and Flask**.
