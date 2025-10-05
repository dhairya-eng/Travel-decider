# app.py
import re
import pandas as pd
import streamlit as st
from model import init_db, save_trip, run_gemini, fetch_recent_trips, build_group_prompt

init_db()
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="centered")
st.title("🌍 AI Travel Planner")
st.caption("Gemini 2.0 Flash • Group Personality Planner")

st.sidebar.header("Mode")
mode = st.sidebar.radio("Plan a trip:", ["Individual", "Group"])


# --------------------------------
# helpers
# --------------------------------
def parse_harmony_score(text: str) -> int:
    """
    Extracts 'Mood Harmony Score: X/10' where X is 1..10.
    Returns X or 0 if not found.
    """
    m = re.search(r"Mood\s*Harmony\s*Score:\s*(\d+)\s*/\s*10", text, flags=re.IGNORECASE)
    if not m:
        return 0
    try:
        val = int(m.group(1))
        return max(0, min(10, val))
    except:
        return 0


# --------------------------------
# Individual Mode
# --------------------------------
if mode == "Individual":
    st.subheader("Individual Trip")
    with st.form("individual_form"):
        col1, col2 = st.columns(2)
        budget = col1.number_input("Budget (USD)", min_value=100, value=1000)
        days = col2.number_input("Trip Duration (days)", min_value=1, value=5)
        col3, col4 = st.columns(2)
        airport = col3.text_input("Nearest Airport / City", value="IAD")
        continent = col4.text_input("Preferred Continent (optional)")
        submitted = st.form_submit_button("Generate Plan")

        if submitted:
            prompt = (
                f"My budget is ${budget}, I want to travel for {days} days, "
                f"and my nearest airport is {airport}. "
            )
            if continent:
                prompt += f"I prefer visiting {continent}. "
            prompt += (
                "Please suggest exactly 3 destinations with approximate costs and a short reason. "
                "End with 'Mood Harmony Score: 7/10' as a placeholder even if solo."
            )

            with st.spinner("Planning your trip..."):
                ai_response = run_gemini(prompt)
                trip_id = save_trip("individual", prompt, ai_response)

            st.success(f"Trip #{trip_id} created")
            st.markdown("### ✈️ AI Suggested Destinations")
            st.markdown(ai_response)

            # optional score bar
            score = parse_harmony_score(ai_response)
            if score:
                st.progress(score / 10)


# --------------------------------
# Group Mode (with Mood)
# --------------------------------
else:
    st.subheader("Group Trip (with Personalities)")
    group_size = st.number_input("Number of Travelers", min_value=2, max_value=10, value=3)

    mood_options = ["Adventure", "Relaxation", "Culture", "Nightlife", "Food & Exploration", "Romantic"]
    members = []

    with st.form("group_form"):
        for i in range(group_size):
            st.markdown(f"#### 👤 Member {i+1}")
            col1, col2 = st.columns(2)
            name = col1.text_input(f"Name {i+1}", value=f"Member {i+1}")
            budget = col2.number_input(f"Budget (USD) {i+1}", min_value=100, value=1000, key=f"budget{i}")
            col3, col4 = st.columns(2)
            airport = col3.text_input(f"Nearest Airport {i+1}", value="IAD", key=f"airport{i}")
            continent = col4.text_input(f"Preferred Continent {i+1} (optional)", key=f"continent{i}")
            mood = st.selectbox(f"Travel Personality {i+1}", mood_options, index=0, key=f"mood{i}")

            members.append({
                "name": name,
                "budget": budget,
                "airport": airport,
                "continent": continent or "unspecified",
                "mood": mood
            })

        days = st.number_input("Trip Duration (days)", min_value=1, value=6)
        submitted = st.form_submit_button("Generate Group Plan")

        if submitted:
            # build prompt with moods
            prompt = build_group_prompt(members, days)

            # show quick mood distribution
            mood_df = pd.DataFrame({"Mood": [m["mood"] for m in members]})
            st.markdown("##### Group Personality Mix")
            st.bar_chart(mood_df["Mood"].value_counts())

            with st.spinner("Balancing group personalities & budget..."):
                ai_response = run_gemini(prompt)
                trip_id = save_trip("group", prompt, ai_response, members)

            st.success(f"Group Trip #{trip_id} saved!")
            st.markdown("### 🧭 AI Suggested Destinations")
            st.markdown(ai_response)

            # show harmony score if model returned it
            score = parse_harmony_score(ai_response)
            if score:
                st.markdown(f"**Mood Harmony Score:** {score}/10")
                st.progress(score / 10)


# --------------------------------
# History
# --------------------------------
st.sidebar.header("🕓 Recent Trips")
history = fetch_recent_trips()
if not history:
    st.sidebar.info("No trips yet.")
else:
    for t in history:
        st.sidebar.markdown(f"**Trip #{t[0]} — {t[1]}**  \n_{t[4]}_")
