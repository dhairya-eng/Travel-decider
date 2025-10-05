# Travel-decider
Perfect ✅ — here’s a **clean, professional, ready-to-publish `README.md`** you can drop straight into your GitHub repo.
It’s written in a style that makes your project stand out (looks great on your profile and for recruiters/investors).

---

# 🌍 AI Travel Planner — *Group Personality Based Trip Planning*

> **AI-powered group travel planner that balances everyone’s travel personalities.**
> Built with **Gemini 2.0 Flash**, **LangGraph**, and **Streamlit**, this app suggests destinations that fit both your **budget** and **mood harmony** across the group.

---

## ✨ Overview

**AI Travel Planner** takes the pain out of group travel decisions by understanding each traveler’s **budget**, **location**, and **personality type**.
It then uses **Google Gemini 2.0 Flash** to generate realistic travel suggestions that satisfy the whole group — with a calculated **Mood Harmony Score (1-10)**.

Whether you’re an **adventurer**, **foodie**, or **romantic traveler**, the app blends everyone’s styles to create the *perfect compromise destination list*.

---

## 🧩 Key Features

| Feature                          | Description                                                                                    |
| -------------------------------- | ---------------------------------------------------------------------------------------------- |
| 🧠 **Group Personality Planner** | Collects each traveler’s mood (Adventure, Relaxation, Culture, etc.) and balances preferences. |
| 💸 **Smart Budget Aggregation**  | Computes group total + average budget and uses that in AI reasoning.                           |
| ✈️ **Gemini 2.0 Flash Powered**  | Fast, cost-efficient reasoning via Google Generative AI.                                       |
| 🎯 **Mood Harmony Score**        | Quantifies how well the suggested destinations match everyone’s personality mix.               |
| 🧾 **SQLite Persistence**        | Stores trip history and group data locally for reuse or personalization.                       |
| 📊 **Streamlit UI**              | Interactive web interface with mood distribution charts and recent-trip sidebar.               |

---

## 🏗️ Tech Stack

* **Frontend / UI:** Streamlit
* **AI Model:** Google Gemini 2.0 Flash (via LangChain)
* **Agent Flow:** LangGraph StateGraph
* **Database:** SQLite (local persistence)
* **Environment Management:** dotenv

---

## 🚀 Quick Start

### 1️⃣ Clone Repo

```bash
git clone https://github.com/<your-username>/ai-travel-planner.git
cd ai-travel-planner
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Environment Variable

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 4️⃣ Run Locally

```bash
streamlit run app.py
```

Visit 👉 [http://localhost:8501](http://localhost:8501)

---

## 🧠 How It Works

1. Each user (or group member) fills:

   * Budget 💰
   * Days 📆
   * Airport ✈️
   * Preferred continent 🌍
   * Personality/mood (e.g., Adventure, Relaxation, Culture …)

2. The backend builds a structured prompt:

   ```text
   A group of 3 people is planning a 6-day trip.
   Total budget $3600 (~$1200/person).
   Airports: IAD, JFK.
   Group personalities: Alice (Adventure), Bob (Culture), Mia (Food & Exploration).
   ```

3. **Gemini 2.0 Flash** analyzes group synergy → suggests 3 destinations.

4. Displays results with reasoning and a **Mood Harmony Score (1-10)**.

5. Stores results in SQLite for future reference.

---

## 🧮 Example Output

> **1. Lisbon, Portugal** — Great mix of food (🍽️) and coastal adventure (🏄). Affordable flights from US East Coast.
> **2. Athens, Greece** — Rich culture for Bob and beautiful relaxation spots for the group.
> **3. Tokyo, Japan** — Perfect for nightlife and food enthusiasts.
> **Mood Harmony Score:** 9/10 🎯

---

## 🗄️ Project Structure

```
ai-travel-planner/
├── app.py          # Streamlit UI (frontend)
├── backend.py      # Gemini + LangGraph + SQLite logic
├── .env            # Google API key
├── requirements.txt
└── README.md
```

---

## ☁️ Deployment (1-Click Streamlit)

1. Push this repo to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. New App → select repo → entry point `app.py`.
4. Add secrets:

   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```
5. Deploy!

Your app will be live at
👉 `https://<your-username>-ai-travel-planner.streamlit.app`

---

## 🧭 Roadmap

* 🔄 Interactive budget slider → AI re-balances suggestions
* 🌦️ Integrate Weather API for real-time conditions
* ✈️ Travelpayouts API for live flight/hotel prices
* 🧠 Persistent AI memory (“Welcome back, Dhairya — last time you went to Prague!”)
* 🤝 Collaborative Room Codes for multi-user sessions
* 📊 Visual Mood Compatibility charts for teams/families

---

## 💡 Why It’s Different

Unlike generic AI trip generators, **AI Travel Planner** uses **group psychology and mood balancing** to build plans that everyone actually agrees on.
It’s not just about destinations — it’s about **group harmony**.

---

## 🧑‍💻 Contributing

Pull requests are welcome!
If you’d like to add a feature (e.g., collaboration mode, flight API integration), please open an issue first to discuss the idea.

---
