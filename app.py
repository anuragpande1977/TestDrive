import streamlit as st
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# ---------------------------
# GOOGLE SHEETS AUTH
# ---------------------------
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
client = gspread.authorize(credentials)
sheet = client.open("Testosterone Index Form (Responses)").sheet1  # Make sure this matches your sheet name

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
# AGE INPUT
# ---------------------------
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# ---------------------------
# QUESTIONNAIRE
# ---------------------------
questions = {
    "Energy & Vitality": {
        "energy": "I often feel low on energy or fatigue during the day.",
        "recovery": "I take longer to recover from exercise or stress.",
        "sleep": "I often wake up feeling unrefreshed or tired."
    },
    "Mood & Motivation": {
        "mood": "My mood is often low or unstable.",
        "focus": "I experience mental fog or difficulty concentrating.",
        "motivation": "I lack motivation for exercise or physical activity."
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
# CALCULATE SCORE
# ---------------------------
if st.button("🚦 Check My Status"):
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

    # Record Data in Google Sheets (with timestamp)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answers = ", ".join([f"{k}:{responses[k]}" for k in responses])
    sheet.append_row([timestamp, name, email, age, percent_score, status, answers])

    st.success("✅ Thank you for using the Test Drive Questionnaire.")

    # ---------------------------
    # REAL COMPARISON DATA
    # ---------------------------
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Ensure correct column names
    if not {"Age", "Status"}.issubset(df.columns):
        st.error("Google Sheet does not have proper column headers (Age, Status). Please fix it.")
    else:
        # Filter for similar age group (±5 years)
        age_filtered = df[(df["Age"] >= age - 5) & (df["Age"] <= age + 5)]

        if len(age_filtered) > 0:
            comparison = age_filtered["Status"].value_counts().reindex(
                ["✅ Healthy", "⚠️ Watch Zone", "🛑 High Symptom Burden"], fill_value=0
            )

            # Chart
            st.markdown("### 📊 How You Compare to Others in Your Age Group")
            fig, ax = plt.subplots()
            ax.bar(comparison.index, comparison.values, color=["#28A745", "#FFC107", "#DC3545"])
            ax.set_ylabel("Number of Users")
            ax.set_xlabel("Status")
            ax.set_title(f"Symptom Status Distribution (Age {age}±5)")
            st.pyplot(fig)
        else:
            st.info("Not enough data yet to show a comparison for your age group.")
