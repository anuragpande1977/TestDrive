import streamlit as st
import matplotlib.pyplot as plt
import urllib.parse

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Test Drive Symptom Checker", layout="centered")
st.title("🚀 Test Drive Symptom Checker")
st.subheader("Find out if your lifestyle signs suggest testosterone-related changes.")

st.markdown("Answer a few quick questions. We'll give you a simple **status** (Healthy, Watch Zone, or High Symptom Burden) and store your results securely.")

# ---------------------------
# AGE INPUT
# ---------------------------
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# ---------------------------
# QUESTIONNAIRE (Grouped)
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
scores_map = {opt: i+1 for i, opt in enumerate(options)}  # 1 to 5 scale

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
    st.markdown(f"<div style='background-color:{color};padding:15px;border-radius:8px;'>"
                f"<h2>{status}</h2>"
                f"<p>{message}</p>"
                "</div>", unsafe_allow_html=True)

    # Flagged Symptoms
    flagged_symptoms = [q for q, resp in responses.items() if scores_map[resp] >= 4]
    if flagged_symptoms:
        st.markdown("### 🚩 Key Areas to Improve")
        for symptom in flagged_symptoms:
            for category, qs in questions.items():
                if symptom in qs:
                    st.markdown(f"- **{qs[symptom]}** ({category})")

    # Age group distribution chart
    mock_distribution = {
        (45, 50): {"Healthy": 25, "Watch Zone": 50, "High Symptom Burden": 25},
        (51, 55): {"Healthy": 20, "Watch Zone": 45, "High Symptom Burden": 35},
        (56, 60): {"Healthy": 15, "Watch Zone": 40, "High Symptom Burden": 45},
        (61, 65): {"Healthy": 10, "Watch Zone": 35, "High Symptom Burden": 55},
    }

    def get_mock_distribution(age):
        for (start, end), dist in mock_distribution.items():
            if start <= age <= end:
                return dist
        return {"Healthy": 20, "Watch Zone": 50, "High Symptom Burden": 30}

    st.markdown("### 📊 How You Compare to Others in Your Age Group")
    dist = get_mock_distribution(age)
    fig, ax = plt.subplots()
    ax.bar(dist.keys(), dist.values(), color=["#28A745", "#FFC107", "#DC3545"])
    ax.set_ylabel("% of Men in Age Group")
    ax.set_xlabel("Status")
    ax.set_title(f"Symptom Status Distribution (Age {age})")
    st.pyplot(fig)

   import urllib.parse

# Prepare data for Google Form submission
answers = ", ".join([f"{k}:{responses[k]}" for k in responses])

form_url = (
    "https://docs.google.com/forms/d/e/1FAIpQLScXUpx545fygIemIvYadB52xupMxCKWD4gA6vY835Uxq1E8Nw/viewform?usp=pp_url"
    f"&entry.111111={urllib.parse.quote(name)}"      # Name
    f"&entry.222222={urllib.parse.quote(email)}"     # Email
    f"&entry.333333={age}"                           # Age
    f"&entry.444444={percent_score}"                 # Score
    f"&entry.555555={urllib.parse.quote(status)}"    # Status
    f"&entry.666666={urllib.parse.quote(answers)}"   # All answers
)

st.markdown(f"[📩 Submit Your Results Securely]({form_url})", unsafe_allow_html=True)
st.success("📝 Your results are ready. Click the link above to save them to our system.")
