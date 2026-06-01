import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timezone

st.set_page_config(page_title="Test Drive Symptom Checker", layout="centered")

# Hide Streamlit UI chrome
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏎️ Test Drive Questionnaire")
st.subheader("Are your lifestyle signs shifting your testosterone balance?")
st.markdown(
    "Answer a few simple questions and find out if you're in the **Healthy Zone**, "
    "**Watch Zone**, or showing a **High Symptom Burden**."
)


# ---------------------------
# SUPABASE CONNECTION (optional / graceful)
# ---------------------------
def _get_secret(key):
    try:
        return st.secrets[key]
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_supabase():
    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_KEY")
    if not url or not key:
        return None
    try:
        from supabase import create_client

        return create_client(url, key)
    except Exception as e:
        st.warning(f"Could not connect to the database: {e}")
        return None


supabase = get_supabase()
TABLE = "responses"

if supabase is None:
    st.info(
        "ℹ️ Running in preview mode — responses are not being saved. "
        "Set SUPABASE_URL and SUPABASE_KEY in secrets to enable saving and progress tracking."
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
        "energy": "I occasionally feel low on energy or fatigue during the day.",
        "recovery": "I take longer to recover from exercise or stress than I did a few years ago.",
        "sleep": "I occasionally wake up feeling unrefreshed or tired.",
    },
    "Mood & Motivation": {
        "mood": "I have occasional negative mood swings and feel emotionally drained.",
        "focus": "I occasionally experience mental fog or difficulty concentrating.",
        "motivation": "I occasionally lack motivation for exercise or physical activity.",
    },
    "Physical Performance": {
        "strength": "I feel a noticeable decline in my strength or endurance than I did a few years ago.",
        "appearance": "I feel dissatisfied with my body composition (muscle vs. fat).",
    },
    "Sexual Health": {
        "libido": "My interest in intimacy has declined.",
    },
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

    total_score = sum(scores_map[resp] for resp in responses.values())
    max_score = len(responses) * 5
    percent_score = int((total_score / max_score) * 100)

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

    st.markdown(
        f"<div style='background-color:{color};padding:15px;border-radius:8px;'>"
        f"<h2>{status}</h2>"
        f"<p>{message}</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    flagged_symptoms = [q for q, resp in responses.items() if scores_map[resp] >= 4]
    if flagged_symptoms:
        st.markdown("### 🚩 Key Areas to Improve")
        for symptom in flagged_symptoms:
            for category, qs in questions.items():
                if symptom in qs:
                    st.markdown(f"- **{qs[symptom]}** ({category})")

    # ---------------------------
    # SAVE TO SUPABASE
    # ---------------------------
    record = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "name": name,
        "email": email,
        "age": int(age),
        "score": percent_score,
        "status": status,
        "answers": {k: responses[k] for k in responses},
    }

    if supabase is not None:
        try:
            supabase.table(TABLE).insert(record).execute()
        except Exception as e:
            st.warning(f"Your result was calculated but could not be saved: {e}")

    # ---------------------------
    # PROGRESS OVER TIME (BEFORE vs AFTER)
    # ---------------------------
    rows = []
    if supabase is not None:
        try:
            res = (
                supabase.table(TABLE)
                .select("created_at, score")
                .eq("email", email)
                .order("created_at")
                .execute()
            )
            rows = res.data or []
        except Exception as e:
            st.warning(f"Could not load your progress history: {e}")

    df = pd.DataFrame(rows)
    if not df.empty and "score" in df.columns and len(df) > 1:
        st.markdown("### 📊 Your Progress Over Time")
        df["created_at"] = pd.to_datetime(df["created_at"])
        df = df.sort_values("created_at")

        fig, ax = plt.subplots()
        ax.bar(df["created_at"].dt.strftime("%Y-%m-%d %H:%M"), df["score"], color="#007BFF")
        ax.set_xlabel("Date")
        ax.set_ylabel("Symptom Score (%)")
        ax.set_title("Your Testosterone Index Progress")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        last_score = int(df["score"].iloc[-2])
        current_score = int(df["score"].iloc[-1])
        change = current_score - last_score

        if change < 0:
            st.success(f"✅ Your symptom score improved by {abs(change)}% since your last check!")
        elif change > 0:
            st.warning(f"⚠️ Your symptom score increased by {change}%. Consider lifestyle improvements.")
        else:
            st.info("ℹ️ No change since your last check.")
    elif supabase is not None:
        st.info("No previous submissions found. Your progress will be tracked from now on.")
