import os
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model, 
                            gemini_pro_vision_response,
                            embedding_model_response,
                            gemini_pro_response)

# Setting up the page configuration
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🌠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to enhance the UI
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    .st-bw {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
    }
    .stButton>button {
        background-color: #4a69bd;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1e3799;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .stTitle {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-weight: bold;
    }
    .stMarkdown {
        color: #f1f2f6;
    }
    .css-1vq4p4l {
        padding: 1rem 1rem 1.5rem !important;
    }
    
    /* Styling for text areas and chat input */
    .stTextArea > div > div > textarea,
    .stChatInputContainer textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }

    /* Styling for text input */
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 5px;
    }

    /* Placeholder text color */
    .stTextArea > div > div > textarea::placeholder,
    .stTextInput > div > div > input::placeholder,
    .stChatInputContainer textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }

    /* Focus state for text areas, inputs, and chat input */
    .stTextArea > div > div > textarea:focus,
    .stTextInput > div > div > input:focus,
    .stChatInputContainer textarea:focus {
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.5);
    }

    /* Adjusting the chat input container */
    .stChatInputContainer {
        background-color: transparent !important;
        padding: 5px !important;
    }

    /* Styling the send button in chat input */
    .stChatInputContainer .stButton > button {
        background-color: #4a69bd !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Function to translate role between Gemini-pro and Streamlit technology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == 'model' else user_role

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Gemini AI",
        options=['ChatBot', 'Image Captioning', 'Embed text', 'Ask me Anything'],
        menu_icon='stars',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "rgba(255, 255, 255, 0.1)"},
            "icon": {"color": "black", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#4a69bd"},
            "nav-link-selected": {"background-color": "#4a69bd"},
        }
    )

# Main content
if selected == "ChatBot":
    model = load_gemini_pro_model()
    
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    st.markdown("<h1 class='stTitle'>🤖 AI ChatBot</h1>", unsafe_allow_html=True)
    st.markdown("### Ask me anything, I'm here to help!")
    
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    user_prompt = st.chat_input("Ask Gemini-Pro")
    
    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)

elif selected == "Image Captioning":
    st.markdown("<h1 class='stTitle'>📷 Snap Narrate</h1>", unsafe_allow_html=True)
    
    uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        
        if st.button("Generate Caption", key="generate_caption"):
            col1, col2 = st.columns(2)
            
            with col1:
                resized_image = image.resize((800, 500))
                st.image(resized_image, use_column_width=True)
            
            default_prompt = "Write a short caption for this image"
            caption = gemini_pro_vision_response(default_prompt, image)
            
            with col2:
                st.info(caption)

elif selected == 'Embed text':
    st.markdown("<h1 class='stTitle'>🔠 Embed Text</h1>", unsafe_allow_html=True)
    
    input_text = st.text_area("", placeholder="Enter the text to get the embedding")
    
    if st.button("Get Embedding", key="get_embedding"):
        response = embedding_model_response(input_text)
        st.markdown(response)

elif selected == 'Ask me Anything':
    st.markdown("<h1 class='stTitle'>❓ Ask me Anything</h1>", unsafe_allow_html=True)
    
    input_prompt = st.text_area("", placeholder="Ask Gemini-Pro...")
    
    if st.button("Get Response", key="get_response"):
        response = gemini_pro_response(input_prompt)
        st.markdown(response)

# Footer
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; width: 100%; background-color: rgba(0,0,0,0.5); color: white; text-align: center; padding: 10px;'>
    Powered by Gemini AI | Created with 💜 by OBITO
</div>
""", unsafe_allow_html=True)