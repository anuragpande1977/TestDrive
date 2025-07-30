import streamlit as st
import matplotlib.pyplot as plt
import urllib.parse

# ---------------------------
# PAGE SETUP
# ---------------------------
st.set_page_config(page_title="Test Drive Symptom Checker", layout="centered")
st.title("🏎️ Test Drive Symptom Checker")
st.subheader("Check if your lifestyle signs could point to testosterone-related changes.")

st.markdown(
    "Answer a few quick questions to see where you stand: **Healthy, Watch Zone, or High Symptom Burden**. "
    "Your results will be shown instantly on this page."
)

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

    # Determine Status (Evidence-based thresholds)
    if percent_score <= 30:
        status = "✅ Healthy"
        color = "#D4EDDA"
        message = "Your lifestyle signs look healthy. Keep up the good habits!"
    elif percent_score <= 50:
        status = "⚠️ Watch Zone"
        color = "#FCF8E3"
        message = "You may have early signs of testosterone-related changes. Consider taking action."
    else:
        status = "🛑 High Symptom Burden"
        color = "#F2DEDE"
        message = "Multiple signs suggest testosterone-related changes. It's time to take control."

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

    # Age group distribution chart based on published data
    distribution_data = {
        (30, 39): {"Healthy": 94, "Watch Zone": 5, "High Symptom Burden": 1},
        (40, 49): {"Healthy": 90, "Watch Zone": 8, "High Symptom Burden": 2},
        (50, 59): {"Healthy": 85, "Watch Zone": 12, "High Symptom Burden": 3},
        (60, 69): {"Healthy": 75, "Watch Zone": 20, "High Symptom Burden": 5},
        (70, 100): {"Healthy": 60, "Watch Zone": 25, "High Symptom Burden": 15},
    }

    def get_distribution(age):
        for (start, end), dist in distribution_data.items():
            if start <= age <= end:
                return dist
        return {"Healthy": 90, "Watch Zone": 8, "High Symptom Burden": 2}

    st.markdown("### 📊 How You Compare to Others in Your Age Group")
    dist = get_distribution(age)
    fig, ax = plt.subplots()
    ax.bar(dist.keys(), dist.values(), color=["#28A745", "#FFC107", "#DC3545"])
    ax.set_ylabel("% of Men in Age Group")
    ax.set_xlabel("Status")
    ax.set_title(f"Symptom Status Distribution (Age {age})")
    st.pyplot(fig)

    # Prepare data for Google Form submission
    answers = ", ".join([f"{k}:{responses[k]}" for k in responses])

    form_url = (
        "https://docs.google.com/forms/d/e/1FAIpQLScXUpx545fygIemIvYadB52xupMxCKWD4gA6vY835Uxq1E8Nw/viewform?usp=pp_url"
        f"&entry.1977894388={urllib.parse.quote(name)}"
        f"&entry.2104446332={urllib.parse.quote(email)}"
        f"&entry.2083902497={age}"
        f"&entry.1267833734={percent_score}"
        f"&entry.766468661={urllib.parse.quote(status)}"
        f"&entry.929729932={urllib.parse.quote(answers)}"
    )

    st.markdown(f"[📩 Save Your Results Securely]({form_url})", unsafe_allow_html=True)
    st.success("📝 Your results are ready. Click the link above if you want to save them.")
