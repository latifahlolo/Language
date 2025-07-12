import streamlit as st
import time
import re

# ✅ تحليل الترجمة مباشرة داخل Streamlit
def analyze_translation(english, arabic):
    if "الآن" not in arabic and "في هذه اللحظة" not in arabic:
        return "❌ الترجمة غير دقيقة: لم تتضمن عنصر الاستمرارية مثل 'الآن' أو 'في هذه اللحظة'."
    elif "قرأت" in arabic or "شاهدت" in arabic or "طبخت" in arabic:
        return "❌ الترجمة خاطئة: استخدمتي الماضي بدلًا من المضارع المستمر."
    else:
        return "✅ الترجمة تبدو دقيقة وتعكس الاستمرارية."

# ✅ كشف اللغة
def detect_language(text):
    english_pattern = re.compile(r'^[A-Za-z0-9\s.,?!\'\";:-]+$')
    arabic_pattern = re.compile(r'^[\u0600-\u06FF\s0-9.,؟!،؛:]+$')
    if english_pattern.fullmatch(text.strip()):
        return "en"
    elif arabic_pattern.fullmatch(text.strip()):
        return "ar"
    return None

# ✅ واجهة Streamlit
st.title("💬 Translation Chatbot")

if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.english_sentence = ""
    st.session_state.arabic_translation = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    with st.chat_message(role):
        st.markdown(content)

if not st.session_state.messages:
    add_message("assistant", "👋 Hello! I’m your translation assistant.")
    add_message("assistant", "Please type the English sentence you'd like to translate.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Type your message here...")

if prompt:
    add_message("user", prompt)

    if st.session_state.step == 1:
        if detect_language(prompt) != "en":
            add_message("assistant", "⚠️ Please enter the sentence in **English** using only English letters.")
        else:
            st.session_state.english_sentence = prompt
            with st.chat_message("assistant"):
                with st.spinner("Assistant is typing..."):
                    time.sleep(1)
                    reply = "Great! Now, please provide the Arabic translation."
                    st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.session_state.step = 2

    elif st.session_state.step == 2:
        if detect_language(prompt) != "ar":
            add_message("assistant", "⚠️ Please enter the translation in **Arabic** using only Arabic letters.")
        else:
            st.session_state.arabic_translation = prompt
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your translation..."):
                    analysis = analyze_translation(
                        st.session_state.english_sentence,
                        st.session_state.arabic_translation
                    )
                    st.markdown(analysis)
            st.session_state.messages.append({"role": "assistant", "content": analysis})
            add_message("assistant", "Would you like to try another sentence? Type it in English to continue.")
            st.session_state.step = 1
