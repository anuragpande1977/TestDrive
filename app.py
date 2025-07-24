import streamlit as st
import pandas as pd
from datetime import datetime

# Page setup
st.set_page_config(page_title="Test Drive Performance Check", layout="centered")
st.title("🚗 Test Drive Performance Check")
st.subheader("Rediscover your energy, confidence, and vitality in under 2 minutes.")

st.markdown("Answer a few quick questions and get your **Performance Score** to see how Test Drive can help reignite your drive.")

# Questions
energy = st.slider("💥 How would you rate your daily energy levels?", 0, 10, 5)
focus = st.slider("🧠 How often do you feel mentally foggy? (Lower = better)", 0, 10, 5)
motivation = st.slider("🏃‍♂️ How motivated do you feel for workouts or physical activity?", 0, 10, 5)
confidence = st.slider("💼 How would you rate your confidence in daily life?", 0, 10, 5)
recovery = st.slider("🔁 How quickly do you recover from exercise or stress?", 0, 10, 5)
mood = st.slider("🙂 How stable is your mood throughout the week?", 0, 10, 5)
appearance = st.slider("💪 How satisfied are you with your body composition (muscle/fat)?", 0, 10, 5)

# Optional user message input
st.markdown("### 💬 Leave a Message (Optional)")
name = st.text_input("Your Name")
email = st.text_input("Your Email")
message = st.text_area("Your Message or Concern")

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
    st.markdown(f"[Click here to email us](mailto:a.pande@valensa.com?subject=Test%20Drive%20Performance%20Score%20{percent_score}&body=Name:%20{name}%0AEmail:%20{email}%0AMessage:%20{message})")

    # Show informational video
    st.markdown("### 🎥 Learn More")
    st.video("https://www.youtube.com/watch?v=YOUR_VIDEO_ID")  # Replace with actual video URL

    st.success("📝 Your response has been processed. You can email us directly for follow-up.")

