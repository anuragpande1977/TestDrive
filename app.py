import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(page_title="Testosterone Lifestyle Index", layout="centered")
st.title("🧩 Testosterone Lifestyle Index")
st.subheader("Rediscover your energy, confidence, and vitality in under 2 minutes.")

st.markdown("Answer these lifestyle questions and get your **Testosterone Lifestyle Score** with targeted feedback.")

# Age input
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# Likert scale options
likert_options = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neither Agree/Disagree": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Questions (based on AMS scale adapted for lifestyle)
questions = {
    "Energy & Motivation": [
        "I often feel tired or lack the drive to get through the day.",
        "I no longer feel as motivated to take on new challenges as I used to."
    ],
    "Mood & Mental Clarity": [
        "I sometimes feel more irritable or easily frustrated than before.",
        "I find it harder to focus or concentrate compared to a few years ago."
    ],
    "Muscle & Strength": [
        "I have noticed a decrease in my muscle strength or ability to perform physical tasks.",
        "I find it harder to maintain or build muscle despite regular exercise."
    ],
    "Sexual Health": [
        "My interest in sexual activity has decreased compared to before.",
        "I am less satisfied with my sexual performance or confidence."
    ],
    "Sleep & Recovery": [
        "I often wake up feeling unrefreshed or lacking energy.",
        "My sleep quality is not as good as it used to be."
    ],
    "Body Composition": [
        "I have gained belly fat despite not changing my eating habits.",
        "It is harder for me to lose weight than it used to be."
    ]
}

# Collect answers
answers = {}
low_score_flags = []

for category, qs in questions.items():
    st.markdown(f"### {category}")
    for q in qs:
        response = st.radio(q, likert_options.keys(), key=q)
        score = likert_options[response]
        answers[q] = score
        if score <= 2:
            low_score_flags.append((category, q))

# Name and email inputs
name = st.text_input("Your Name")
email = st.text_input("Your Email")

if st.button("🚦 Calculate My Score"):
    total_score = sum(answers.values())
    max_score = len(answers) * 5
    percent_score = int((total_score / max_score) * 100)

    # Show score
    st.markdown(f"## 💪 Your Testosterone Lifestyle Score: <span style='color:black; font-weight:bold;'>{percent_score}/100</span>", unsafe_allow_html=True)

    # Recommendations based on score
    if percent_score >= 80:
        st.markdown("<div style='background-color:#ff0000;padding:10px;border-radius:5px'><strong>🔥 Peak Performer in Progress</strong><br>Keep the momentum going! Test Drive can help you optimize further.</div>", unsafe_allow_html=True)
    elif percent_score >= 60:
        st.markdown("<div style='background-color:#FCF8E3;padding:10px;border-radius:5px'><strong>⚠️ Your Engine Needs Tuning</strong><br>You're on the edge — Test Drive can help restore your drive, mood, and energy.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#F2DEDE;padding:10px;border-radius:5px'><strong>🛑 Time to Reignite Your Drive</strong><br>You're not alone — many men feel this way. Test Drive is scientifically designed to help you reboot.</div>", unsafe_allow_html=True)

    # Specific low-score feedback
    if low_score_flags:
        st.markdown("### 🎯 Areas Where You May Benefit Most")
        for category, question in low_score_flags:
            st.markdown(f"- **{category}**: {question}")

    # About Test Drive
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

    # Email option
    st.markdown("📩 _Send us your message directly._")
    st.markdown(f"[Click here to email us](mailto:a.pande@valensa.com?subject=Testosterone%20Lifestyle%20Score%20{percent_score}&body=Name:%20{name}%0AEmail:%20{email})")

    # Mock distribution data by age group
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
        return {"0-40": 20, "41-60": 50, "61-80": 20, "81-100": 10}

    st.markdown("### 📊 How Your Score Compares to Others in Your Age Group")
    dist = get_mock_distribution(age)
    fig, ax = plt.subplots()
    ax.bar(dist.keys(), dist.values(), color="#4C72B0")
    ax.set_ylabel("% of Men in Age Group")
    ax.set_xlabel("Score Range")
    ax.set_title(f"Mock Testosterone Lifestyle Score Distribution (Age {age})")
    st.pyplot(fig)

    st.success("📝 Your response has been processed. You can email us directly for follow-up.")

