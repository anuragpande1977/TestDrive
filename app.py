import streamlit as st

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

