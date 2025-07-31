import streamlit as st
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import pandas as pd

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
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
client = gspread.authorize(creds)

try:
    sheet = client.open("Testosterone Index Responses").sheet1  # new dedicated sheet
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
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty and "Score" in df.columns and "Age" in df.columns:
        age_group = df[(df["Age"] >= age - 5) & (df["Age"] <= age + 5)]
        if not age_group.empty:
            counts = age_group["Status"].value_counts().to_dict()
            dist = {
                "Healthy": counts.get("✅ Healthy", 0),
                "Watch Zone": counts.get("⚠️ Watch Zone", 0),
                "High Symptom Burden": counts.get("🛑 High Symptom Burden", 0)
            }

            st.markdown("### 📊 How You Compare to Others in Your Age Group")
            fig, ax = plt.subplots()
            ax.bar(dist.keys(), dist.values(), color=["#28A745", "#FFC107", "#DC3545"])
            ax.set_ylabel("Number of Men in Age Group")
            ax.set_xlabel("Status")
            ax.set_title(f"Symptom Status Distribution (Age {age})")
            st.pyplot(fig)
        else:
            st.info("No comparative data yet for your age group.")
    else:
        st.info("No data available yet for comparison.")

    st.success("✅ Your response has been saved successfully.")
