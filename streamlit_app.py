import streamlit as st
import requests
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Idioms & Phrases Meanings",
    layout="wide"
)

# ---------------- PASTEL CSS ----------------
st.markdown("""
<style>

/* Gradient Background */
.stApp {
    background: linear-gradient(180deg, #f7f2ff 0%, #fff0f8 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #eadcff;
    padding: 15px;
}

/* Sidebar Card */
.sidebar-card {
    background-color: #f3ebff;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 3px 8px rgba(0,0,0,0.05);
}

/* Header strip */
.header-strip {
    background-color: #efe6ff;
    padding: 15px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

/* Supported language banner */
.language-banner {
    background-color: #f3ebff;
    padding: 10px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
    font-size: 16px;
}

/* Input styling */
.stTextInput input {
    background-color: #f3ebff !important;
    border-radius: 18px !important;
    border: 1px solid #d6c6ff !important;
    padding: 12px !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #c7b3ff, #e0c3fc);
    color: white;
    border-radius: 18px;
    padding: 10px 30px;
    font-weight: 600;
    border: none;
}

/* Result cards */
.card {
    background-color: #f3ebff;
    padding: 20px;
    border-radius: 20px;
    margin-top: 15px;
    box-shadow: 0 5px 12px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)

st.sidebar.title("🌸 Idioms Explorer")
st.sidebar.markdown("""
Enter any idiom or phrase to see:

📘 Literal Meaning  
💡 Actual Meaning  
🌍 Cultural Meaning  
""")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

# ⭐ Supported Languages Sidebar Card
st.sidebar.markdown("""
<div class='sidebar-card'>
🌐 <b>Supported Languages</b><br><br>
🇬🇧 English ↔ 🇮🇳 Marathi<br><br>
<i>More languages coming soon ✨</i>
</div>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<div class="header-strip">
<h1>🔍 Idioms & Phrases Meanings</h1>
</div>
""", unsafe_allow_html=True)



# ---------------- CENTER LAYOUT ----------------
col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.subheader("✨ Enter Idiom")

    user_input = st.text_input(
        "",
        placeholder="Example: Break the ice, Once in a blue moon, Hoping against hope..."
    )

    if st.button("💡 Get Meaning"):

        if user_input.strip() == "":
            st.warning("Please enter an idiom.")
        else:

            try:
                detected_lang = detect(user_input)

                # ⭐ Smart language restriction
                if detected_lang not in ["en", "mr"]:
                    st.warning("⚠️ Currently only English and Marathi idioms are supported.")
                    st.stop()

                response = requests.post(
                    "http://127.0.0.1:5000/translate",
                    json={"text": user_input}
                )

                if response.status_code == 200:
                    data = response.json()

                    if "message" in data:
                        st.warning(data["message"])
                    else:

                        st.markdown(
                            f"<div class='card'>🌍 <b>Detected Language:</b> {detected_lang}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='card'>⭐ <b>Similarity Score:</b> {data['similarity_score']}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='card'>📘 <b>Literal Meaning:</b><br>{data['literal_translation']}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='card'>💡 <b>Actual Meaning:</b><br>{data['actual_meaning']}</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            f"<div class='card'>🌏 <b>Cultural Meaning:</b><br>{data['cultural_translation']}</div>",
                            unsafe_allow_html=True
                        )

                else:
                    st.error("Backend server not responding.")

            except:
                st.error("Language detection failed. Please try again.")
