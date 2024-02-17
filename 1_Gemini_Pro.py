

import google.generativeai as genai
import streamlit as st
import time
import random
from utils import SAFETY_SETTTINGS


# 设置用户名和密码
username = "admin"
password = "password"

# 创建登录表单
form = st.form("login_form")
username_input = form.text_input("用户名")
password_input = form.text_input("密码", type="password")
submit_button = form.form_submit_button("登录")

# 验证用户名和密码
if submit_button:
    if username_input == username and password_input == password:
        st.success("登录成功！")
    else:
        st.error("用户名或密码错误！")

st.set_page_config(
    page_title="Chat To XYthing",
    page_icon="🔥",
    menu_items={
        'About': "# Make By hiliuxg"
    }
)

st.title("Chat To XYthing")
st.caption("a chatbot, powered by google gemini pro.")


if "app_key" not in st.session_state:
    # app_key = st.text_input("Your Gemini App Key", type='password')
    # if app_key:
    st.session_state.app_key = "AIzaSyAU8RxYbB6FGA3Ovrl4SL_goC8bj2WVsfo"

if "history" not in st.session_state:
    st.session_state.history = []

try:
    genai.configure(api_key = st.session_state.app_key)
except AttributeError as e:
    st.warning("Please Put Your Gemini App Key First.")

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history = st.session_state.history)

with st.sidebar:
    if st.button("Clear Chat Window", use_container_width = True, type="primary"):
        st.session_state.history = []
        st.rerun()
    
for message in chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

if "app_key" in st.session_state:
    if prompt := st.chat_input(""):
        prompt = prompt.replace('\n', '  \n')
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            try:
                full_response = ""
                for chunk in chat.send_message(prompt, stream=True, safety_settings = SAFETY_SETTTINGS):
                    word_count = 0
                    random_int = random.randint(5, 10)
                    for word in chunk.text:
                        full_response += word
                        word_count += 1
                        if word_count == random_int:
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "_")
                            word_count = 0
                            random_int = random.randint(5, 10)
                message_placeholder.markdown(full_response)
            except genai.types.generation_types.BlockedPromptException as e:
                st.exception(e)
            except Exception as e:
                st.exception(e)
            st.session_state.history = chat.history