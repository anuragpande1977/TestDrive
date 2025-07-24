import streamlit as st
import pandas as pd
import os
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

    st.markdown(f"## 🧠 Your Performance Score: **{percent_score}/100**")

    if percent_score >= 80:
        st.success("🔥 **Peak Performer in Progress**\nKeep the momentum going! Test Drive can help you optimize further.")
    elif percent_score >= 60:
        st.warning("⚠️ **Your Engine Needs Tuning**\nYou're on the edge — Test Drive can help restore your drive, mood, and energy.")
    else:
        st.error("🛑 **Time to Reignite Your Drive**\nYou're not alone — many men feel this way. Test Drive is scientifically designed to help you reboot.")

    st.markdown("### ✅ About Test Drive")
    st.markdown("""
- Formulated for men 40+ dealing with declining energy and drive  
- Supports testosterone balance, mood, and vitality  
- Backed by clinical science  
- All Natural
""")

    st.markdown("📩 _Ask us how to get started with Test Drive today._")

    # Show informational video
    st.markdown("### 🎥 Learn More")
    st.video("https://youtu.be/RmMn4yckQ2Q")  # Replace with actual video URL

    # Save data locally
    record = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Email": email,
        "Message": message,
        "Score": percent_score
    }

    df = pd.DataFrame([record])
    if not os.path.exists("visitor_data.csv"):
        df.to_csv("visitor_data.csv", index=False)
    else:
        df.to_csv("visitor_data.csv", mode='a', index=False, header=False)

    st.success("📝 Your response has been recorded. We'll reach out if you left a message.")
