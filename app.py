import streamlit as st
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt
import numpy as np

# Page setup
st.set_page_config(page_title="Test Drive Performance Check", layout="centered")
st.title("🚗 Test Drive Performance Check")
st.subheader("Rediscover your energy, confidence, and vitality in under 2 minutes.")

st.markdown("Answer a few quick questions and get your **Performance Score** to see how Test Drive can help reignite your drive.")

# Age input
age = st.number_input("📅 Enter your age:", min_value=18, max_value=100, value=45)

# Questions
energy = st.slider("💥 How would you rate your daily energy levels?", 0, 10, 5)
focus = st.slider("🧠 How often do you feel mentally foggy? (Lower = better)", 0, 10, 5)
motivation = st.slider("🏃‍♂️ How motivated do you feel for workouts or physical activity?", 0, 10, 5)
confidence = st.slider("💼 How would you rate your confidence in daily life?", 0, 10, 5)
recovery = st.slider("🔁 How quickly do you recover from exercise or stress?", 0, 10, 5)
mood = st.slider("🙂 How stable is your mood throughout the week?", 0, 10, 5)
appearance = st.slider("💪 How satisfied are you with your body composition (muscle/fat)?", 0, 10, 5)

# Name and email inputs
name = st.text_input("Your Name")
email = st.text_input("Your Email")

if st.button("🚦 Calculate My Score"):
    total_score = energy + (10 - focus) + motivation + confidence + recovery + mood + appearance
    percent_score = int((total_score / 70) * 100)

    st.markdown(f"## 🧠 Your Performance Score: <span style='color:black; font-weight:bold;'>{percent_score}/100</span>", unsafe_allow_html=True)

    if percent_score >= 80:
        st.markdown("<div style='background-color:#DFF0D8;padding:10px;border-radius:5px'><strong>🔥 Peak Performer in Progress</strong><br>Keep the momentum going! Test Drive can help you optimize further.</div>", unsafe_allow_html=True)
    elif percent_score >= 60:
        st.markdown("<div style='background-color:#FCF8E3;padding:10px;border-radius:5px'><strong>⚠️ Your Engine Needs Tuning</strong><br>You're on the edge — Test Drive can help restore your drive, mood, and energy.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#F2DEDE;padding:10px;border-radius:5px'><strong>🛑 Time to Reignite Your Drive</strong><br>You're not alone — many men feel this way. Test Drive is scientifically designed to help you reboot.</div>", unsafe_allow_html=True)

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

    st.markdown("📩 _Send us your message directly._")
    st.markdown(f"[Click here to email us](mailto:a.pande@valensa.com?subject=Test%20Drive%20Performance%20Score%20{percent_score}&body=Name:%20{name}%0AEmail:%20{email})")

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
        return {"0-40": 20, "41-60": 50, "61-80": 20, "81-100": 10}  # default fallback

    st.markdown("### 📊 How Your Score Compares to Others in Your Age Group")
    dist = get_mock_distribution(age)
    fig, ax = plt.subplots()
    ax.bar(dist.keys(), dist.values(), color="#4C72B0")
    ax.set_ylabel("% of Men in Age Group")
    ax.set_xlabel("Score Range")
    ax.set_title(f"Mock Performance Score Distribution (Age {age})")
    st.pyplot(fig)

    # Show informational video
    st.markdown("### 🎥 Learn More")
    st.video("https://youtu.be/RmMn4yckQ2Q")  # Replace with actual video URL

    st.success("📝 Your response has been processed. You can email us directly for follow-up.")

