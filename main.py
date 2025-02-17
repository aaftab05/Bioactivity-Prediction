import home, account, about,chatbot
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import os

GEMINI_API_KEY="AIzaSyAzUFT7V1j7BFZcCNxklFdevko6fWRdkDo"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"

import google.generativeai as genai

genai.configure(api_key="AIzaSyAzUFT7V1j7BFZcCNxklFdevko6fWRdkDo")
model = genai.GenerativeModel("gemini-1.5-flash")


# Set page configuration
st.set_page_config(
    page_title="BIOACTIVITY PREDICTION APP",
)

# Google Analytics integration
st.markdown(
    """
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src=f"https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', os.getenv('analytics_tag'));
        </script>
    """, unsafe_allow_html=True,
)
print(os.getenv('analytics_tag'))





class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='BIOACTIVITY PREDICTION APP',
                options=['Home', 'Account', 'About', 'Chatbot'],
                icons=['house-fill', 'person-circle', 'info-circle-fill', 'chat-left-text-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                styles={
                    "container": {"padding": "5!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        if app == "Home":
            home.app()
        elif app == "Account":
            account.app()
        elif app == "About":
            about.app()
        elif app == "Chatbot":
            chatbot.app()


# Run the application
app = MultiApp()
app.run()
