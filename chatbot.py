import home, account, about
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import os

GEMINI_API_KEY="AIzaSyAzUFT7V1j7BFZcCNxklFdevko6fWRdkDo"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

import google.generativeai as genai

def chatbot_ui():
    st.markdown("### 💬 Chatbot")  # Chatbot header
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_message = st.text_input("Ask me anything!", key="user_message")
    if st.button("Send"):
        if user_message.strip():
            response = get_chatbot_response(user_message)
            if response:
                st.session_state["chat_history"].append(f"You: {user_message}")
                st.session_state["chat_history"].append(f"Bot: {response}")
            else:
                st.session_state["chat_history"].append(f"You: {user_message}")
                st.session_state["chat_history"].append(f"Bot: Sorry, there was an error processing your request.")

    if st.session_state["chat_history"]:
        for chat in st.session_state["chat_history"]:
            st.write(chat)

def get_chatbot_response(user_message):
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": [{"parts":[{"text": user_message}]}]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10) #added timeout
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()
        if 'candidates' in response_json and response_json['candidates']:
          return response_json['candidates'][0]['content']['parts'][0]['text']
        else:
          return "I'm sorry, I couldn't generate a response."
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the Gemini API: {e}")
        return None  # Or handle the error as needed
    except (KeyError, IndexError, TypeError) as e:
        st.error(f"Error parsing the Gemini API response: {e}. Raw response: {response.text if 'response' in locals() else 'No response received'}")
        return None
    
def app():
  """
  This function defines the layout and content of the chatbot page.
  """
  chatbot_ui()

