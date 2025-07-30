import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Test Drive Testosterone Index", layout="centered")
st.title("🚀 Test Drive Testosterone Index")
st.subheader("Rediscover your energy, confidence, and vitality in under 2 minutes.")

st.markdown("Answer a few quick questions and get your **Testosterone Index** to see how Test Drive can help reignite your drive.")

# ---------------------------
# AGE INPUT
# ---------------------------
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# ---------------------------
# QUESTIONNAIRE (Likert Scale: Strongly Disagree to Strongly Agree)
# ---------------------------
questions = {
    "energy": "💥 I often feel low on energy or fatigue during the day.",
    "focus": "🧠 I experience mental fog or difficulty concentrating.",
    "motivation": "🏋️‍♂️ I lack motivation for exercise or physical activity.",
    "confidence": "💼 I feel my confidence has decreased over time.",
    "recovery": "🔁 I take longer to recover from exercise or stress.",
    "mood": "🙂 My mood is often low or unstable.",
    "appearance": "💪 I feel dissatisfied with my body composition (muscle vs. fat).",
    "libido": "❤️ My interest in intimacy has declined.",
    "sleep": "😴 I often wake up feeling unrefreshed or tired.",
    "strength": "🏋️‍♂️ I feel a noticeable decline in my strength or endurance.",
}

options = ["Strongly Disagree", "Disagree", "Neither Agree/Disagree", "Agree", "Strongly Agree"]
scores_map = {opt: i+1 for i, opt in enumerate(options)}  # 1 to 5 scale

responses = {}
for key, q in questions.items():
    responses[key] = st.radio(q, options, index=2)  # Default to "Neither Agree/Disagree"

# ---------------------------
# NAME AND EMAIL
# ---------------------------
name = st.text_input("Your Name")
email = st.text_input("Your Email")

# ---------------------------
# CALCULATE SCORE
# ---------------------------
if st.button("🚦 Calculate My Testosterone Index"):
    total_score = sum([scores_map[resp] for resp in responses.values()])
    max_score = len(questions) * 5
    percent_score = int((total_score / max_score) * 100)

    # Display Score
    st.markdown(f"## 💪 Your Testosterone Index: <span style='color:black; font-weight:bold;'>{percent_score}/100</span>", unsafe_allow_html=True)

    # Interpretation (Low = Good, High = Bad)
    if percent_score <= 40:
        st.markdown("<div style='background-color:#D4EDDA;padding:10px;border-radius:5px'><strong>✅ Healthy Range</strong><br>Your testosterone-related lifestyle indicators look good. Keep it up!</div>", unsafe_allow_html=True)
    elif percent_score <= 60:
        st.markdown("<div style='background-color:#FCF8E3;padding:10px;border-radius:5px'><strong>⚠️ Watch Zone</strong><br>You're showing some early signs. Test Drive may help optimize your vitality.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#F2DEDE;padding:10px;border-radius:5px'><strong>🛑 High Symptom Burden</strong><br>You're likely experiencing testosterone-related effects. Test Drive is designed to help.</div>", unsafe_allow_html=True)

    # ---------------------------
    # SYMPTOM FLAGGING
    # ---------------------------
    flagged_symptoms = [q for q, resp in responses.items() if scores_map[resp] >= 4]
    if flagged_symptoms:
        st.markdown("### 🚩 Key Areas to Improve")
        for symptom in flagged_symptoms:
            st.markdown(f"- {questions[symptom]}")

    # ---------------------------
    # AGE GROUP DISTRIBUTION CHART
    # ---------------------------
    mock_distribution = {
        (45, 50): {"0-40": 25, "41-60": 50, "61-80": 15, "81-100": 10},
        (51, 55): {"0-40": 30, "41-60": 45, "61-80": 20, "81-100": 5},
        (56, 60): {"0-40": 35, "41-60": 40, "61-80": 20, "81-100": 5},
        (61, 65): {"0-40": 40, "41-60": 40, "61-80": 15, "81-100": 5},
    }

    def get_mock_distribution(age):
        for (start, end), dist in mock_distribution.items():
            if start <= age <= end:
                return dist
        return {"0-40": 20, "41-60": 50, "61-80": 20, "81-100": 10}  # fallback

    st.markdown("### 📊 How Your Score Compares to Others in Your Age Group")
    dist = get_mock_distribution(age)
    fig, ax = plt.subplots()
    ax.bar(dist.keys(), dist.values(), color="#4C72B0")
    ax.set_ylabel("% of Men in Age Group")
    ax.set_xlabel("Score Range")
    ax.set_title(f"Mock Testosterone Index Distribution (Age {age})")
    st.pyplot(fig)

    # ---------------------------
    # ABOUT TEST DRIVE
    # ---------------------------
    st.markdown("<div style='background-color:#E8F4FD;padding:15px;border-radius:8px;margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#005A9C;'>✅ About Test Drive</h3>", unsafe_allow_html=True)
    st.markdown("""
    <ul style='font-weight:bold;'>
      <li>Formulated for men 40+ dealing with declining energy and drive</li>
      <li>Supports testosterone balance, mood, and vitality</li>
      <li>Backed by clinical science</li>
      <li>All Natural</li>
    </ul>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------
    # EMAIL LINK
    # ---------------------------
    st.markdown("📩 _Send us your message directly._")
    st.markdown(f"[Click here to email us](mailto:a.pande@valensa.com?subject=Test%20Drive%20Testosterone%20Index%20{percent_score}&body=Name:%20{name}%0AEmail:%20{email})")

    # ---------------------------
    # INFORMATIONAL VIDEO
    # ---------------------------
    st.markdown("### 🎥 Learn More")
    st.video("https://youtu.be/RmMn4yckQ2Q")  # Replace with actual video URL

    st.success("📝 Your response has been processed. You can email us directly for follow-up.")

