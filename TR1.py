import streamlit as st
from openai import OpenAI
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import anthropic
import os


openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
anthropic_client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
credentials = service_account.Credentials.from_service_account_file(st.secrets["gcp_service_account"])

# Initialize Google Cloud Translate client with credentials
translate_client = translate.Client(credentials=credentials)

st.title("Multilingual Translator App")
st.write("Translate text into English using your preferred AI model!")

source_text = st.text_area("Enter the text you want to translate:", height=150)
translation_option = st.radio("Choose Translation Method:", ["GPT-4o-mini", "Claude Haiku", "Google Translate API"])
system_prompt = "Translate the following text to English while maintaining its original meaning and tone. ONLY OUTPUT THE TRANSLATED TEXT AND NOTHING ELSE!"
temperature = st.sidebar.slider("Translation Creativity (Temperature)", 0.0, 1.0, 0.5)

# Button to trigger translation
if st.button("Translate") and source_text:
    translation = None
    
    if translation_option == "GPT-4o-mini":
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": source_text}
            ],
            temperature=temperature
        )
        translation = completion.choices[0].message.content
        
    elif translation_option == "Claude Haiku":
        message= anthropic_client.messages.create(
            model="claude-3-5-haiku-20241022",
            temperature=temperature,
            max_tokens=2048,
            system=system_prompt,
            messages=[
                {"role": "user", "content": source_text}
            ]
        )
        translation = message.content[0].text
        
    elif translation_option == "Google Translate API":
        result = translate_client.translate(source_text, target_language='en')
        translation = result['translatedText']
    
    st.subheader("Translated Text to English")
    st.write(translation)
else:
    st.write("Enter text and select a translation option to begin.")
