import streamlit as st
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd
st.set_page_config(
    page_title="Herb's Forest App",
    page_icon="🌿",
    layout="wide"
)

# Hide Streamlit UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Test Drive Symptom Checker", layout="centered")
st.title("🏎️ Test Drive Questionnaire")
st.subheader("Are your lifestyle signs shifting your testosterone balance?")

st.markdown(
    "Answer a few simple questions and find out if you're in the **Healthy Zone**, "
    "**Watch Zone**, or showing a **High Symptom Burden**."
)

# ---------------------------
# GOOGLE SHEET CONNECTION
# ---------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

try:
    sheet = client.open("TestDriveSheet").sheet1  # <-- Your new sheet name
except Exception as e:
    st.error(f"Could not open the sheet. Check name or permissions. Error: {e}")
    st.stop()


# ---------------------------
# AGE INPUT
# ---------------------------
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# ---------------------------
# QUESTIONNAIRE
# ---------------------------
questions = {
    "Energy & Vitality": {
        "energy": "I ocassionally feel low on energy or fatigue during the day.",
        "recovery": "I take longer to recover from exercise or stress, than i did few years ago.",
        "sleep": "I ocassionallyI have oc wake up feeling unrefreshed or tired."
    },
    "Mood & Motivation": {
        "mood": "I have occassional negative mood swinges and feel emotionally drained",
        "focus": "I experience mental fog or difficulty concentrating.",
        "motivation": "I ocassionally lack motivation for exercise or physical activity."
    },
    "Physical Performance": {
        "strength": "I feel a noticeable decline in my strength or endurance.",
        "appearance": "I feel dissatisfied with my body composition (muscle vs. fat)."
    },
    "Sexual Health": {
        "libido": "My interest in intimacy has declined."
    }
}

options = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
scores_map = {opt: i + 1 for i, opt in enumerate(options)}

responses = {}

st.markdown("## 📝 Questionnaire")
for category, qs in questions.items():
    st.markdown(f"### {category}")
    for key, q in qs.items():
        responses[key] = st.radio(q, options, index=2, key=key)

# ---------------------------
# NAME AND EMAIL
# ---------------------------
st.markdown("---")
name = st.text_input("Your Name")
email = st.text_input("Your Email")

# ---------------------------
# CALCULATE SCORE & SAVE
# ---------------------------
if st.button("🚦 Check My Status"):
    if not name or not email:
        st.error("Please enter both name and email.")
        st.stop()

    total_score = sum([scores_map[resp] for resp in responses.values()])
    max_score = len(responses) * 5
    percent_score = int((total_score / max_score) * 100)

    # Determine Status
    if percent_score <= 40:
        status = "✅ Healthy"
        color = "#D4EDDA"
        message = "Your lifestyle signs look healthy. Keep it up!"
    elif percent_score <= 60:
        status = "⚠️ Watch Zone"
        color = "#FCF8E3"
        message = "You may have early signs related to testosterone decline. Test Drive may help you optimize."
    else:
        status = "🛑 High Symptom Burden"
        color = "#F2DEDE"
        message = "You are showing multiple signs of testosterone-related effects. Test Drive can help you restore your vitality."

    # Display Result
    st.markdown(
        f"<div style='background-color:{color};padding:15px;border-radius:8px;'>"
        f"<h2>{status}</h2>"
        f"<p>{message}</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Flagged Symptoms
    flagged_symptoms = [q for q, resp in responses.items() if scores_map[resp] >= 4]
    if flagged_symptoms:
        st.markdown("### 🚩 Key Areas to Improve")
        for symptom in flagged_symptoms:
            for category, qs in questions.items():
                if symptom in qs:
                    st.markdown(f"- **{qs[symptom]}** ({category})")

    # ---------------------------
    # APPEND TO GOOGLE SHEET
    # ---------------------------
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answers = ", ".join([f"{k}:{responses[k]}" for k in responses])

    sheet.append_row([timestamp, name, email, age, percent_score, status, answers])

    # ---------------------------
    # COMPARATIVE DATA
    # ---------------------------
    # ---------------------------
# COMPARISON FOR SAME USER (BEFORE vs AFTER)
# ---------------------------
# ---------------------------
# COMPARISON FOR SAME USER (BEFORE vs AFTER)
# ---------------------------
data = sheet.get_all_records()
df = pd.DataFrame(data)

if not df.empty and "Email" in df.columns and "Score" in df.columns:
    user_data = df[df["Email"] == email].sort_values("Timestamp")

    if len(user_data) > 1:
        st.markdown("### 📊 Your Progress Over Time")

        fig, ax = plt.subplots()
        ax.bar(user_data["Timestamp"], user_data["Score"], color="#007BFF")
        ax.set_xlabel("Date")
        ax.set_ylabel("Symptom Score (%)")
        ax.set_title("Your Testosterone Index Progress")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        last_score = user_data["Score"].iloc[-2]
        current_score = user_data["Score"].iloc[-1]
        change = current_score - last_score

        # Lower score is better
        if change < 0:
            st.success(f"✅ Your symptom score improved by {abs(change)}% since your last check!")
        elif change > 0:
            st.warning(f"⚠️ Your symptom score increased by {change}%. Consider lifestyle improvements.")
        else:
            st.info("ℹ️ No change since your last check.")
    else:
        st.info("No previous submissions found. Your progress will be tracked from now on.")
else:
    st.info("No data available for progress tracking.")
