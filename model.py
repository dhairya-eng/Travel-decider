# backend.py
import os
import sqlite3
from typing import List, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
DB_PATH = "travel_planner.db"


# ===============================
# DB helpers
# ===============================
def _column_exists(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table});")
    return any(row[1] == column for row in cur.fetchall())

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # trips table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT,
            description TEXT,
            ai_response TEXT,
            created_at TEXT
        );
    """)
    # group_members table (now includes mood)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER,
            name TEXT,
            budget REAL,
            airport TEXT,
            continent TEXT,
            mood TEXT,
            FOREIGN KEY(trip_id) REFERENCES trips(id)
        );
    """)
    # migration: add mood column if old DB exists without it
    if not _column_exists(conn, "group_members", "mood"):
        try:
            cur.execute("ALTER TABLE group_members ADD COLUMN mood TEXT;")
        except sqlite3.OperationalError:
            pass
    conn.commit()
    conn.close()

def save_trip(
    mode: str,
    description: str,
    ai_response: str,
    members: Optional[List[dict]] = None
) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO trips (mode, description, ai_response, created_at) VALUES (?, ?, ?, ?)",
        (mode, description, ai_response, datetime.now().isoformat())
    )
    trip_id = cur.lastrowid

    if mode == "group" and members:
        for m in members:
            cur.execute(
                "INSERT INTO group_members (trip_id, name, budget, airport, continent, mood) VALUES (?, ?, ?, ?, ?, ?)",
                (trip_id, m["name"], float(m["budget"]), m["airport"], m.get("continent", "unspecified"), m.get("mood", "unspecified"))
            )

    conn.commit()
    conn.close()
    return trip_id

def fetch_recent_trips(limit: int = 5):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, mode, description, ai_response, created_at FROM trips ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows


# ===============================
# Gemini + LangGraph
# ===============================
def get_model() -> ChatGoogleGenerativeAI:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY not found in environment/.env")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        max_output_tokens=1024,
        top_p=0.8,
        api_key=api_key,
    )

def build_graph():
    from typing import TypedDict, Optional
    from langchain_core.messages import BaseMessage

    class AgentState(TypedDict):
        user_input: str
        response: Optional[str]

    def call_model(state: "AgentState", config: RunnableConfig):
        model: ChatGoogleGenerativeAI = config["metadata"]["__model__"]
        system_prompt = SystemMessage(
            content=(
                "You are a concise, practical AI travel planner. "
                "User input may describe an individual or a group with travel personalities. "
                "Suggest exactly 3 destinations. For each: give a short reason, "
                "rough flight+lodging cost, and how it matches the group's mix of personalities. "
                "End with a line: 'Mood Harmony Score: X/10' (integer 1-10)."
            )
        )
        user_msg = HumanMessage(content=state["user_input"])
        result = model.invoke([system_prompt, user_msg], config=config)
        return {"response": result.content}

    graph = StateGraph(AgentState)
    graph.add_node("model", call_model)
    graph.set_entry_point("model")
    graph.add_edge("model", END)
    return graph.compile()

def run_gemini(prompt: str) -> str:
    model = get_model()
    graph = build_graph()
    config = RunnableConfig(metadata={"__model__": model})
    init_state = {"user_input": prompt, "response": None}
    result = graph.invoke(init_state, config=config)
    return result.get("response") or ""

# Optional utility: builds a good group prompt including moods
def build_group_prompt(members: List[dict], days: int) -> str:
    total_budget = sum(float(m["budget"]) for m in members)
    avg_budget = round(total_budget / len(members), 2)
    airports = ", ".join({m["airport"] for m in members})
    continents = ", ".join({m["continent"] for m in members if m.get("continent") and m["continent"] != "unspecified"})
    mood_summary = ", ".join([f"{m['name']} ({m.get('mood','unspecified')})" for m in members])

    prompt = (
        f"A group of {len(members)} people is planning a {days}-day trip. "
        f"Total combined budget: ${total_budget} (~${avg_budget}/person). "
        f"Nearest airports: {airports}. "
        f"Group personalities: {mood_summary}. "
    )
    if continents:
        prompt += f"Preferred regions: {continents}. "
    prompt += (
        "Suggest 3 destinations balancing everyone's personalities with estimated total cost, "
        "flight feasibility from these airports, and a brief reason for each. "
        "End with 'Mood Harmony Score: X/10'."
    )
    return prompt
