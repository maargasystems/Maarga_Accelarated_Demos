import os, streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.serpapi import SerpApiTools
from textwrap import dedent

REQUIRED_ENV = ["OPENROUTER_API_KEY", "SERP_API_KEY"]
miss = [v for v in REQUIRED_ENV if not os.getenv(v)]
if miss: st.error(f"Missing env: {', '.join(miss)}"); st.stop()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
SERP_API_KEY   = os.environ["SERP_API_KEY"]

def render_travel_planner():
    st.header("✈️ AI Travel Planner")

    dest = st.text_input("Destination")
    days = st.number_input("Days", 1, 30, 7)

    if st.button("Create itinerary") and dest:
        researcher = Agent(
            model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                             api_key=OPENROUTER_API_KEY),
            tools=[SerpApiTools(api_key=SERP_API_KEY)],
            instructions=[dedent("""\
                Generate 3 search terms → search Google → pick 10 best results.
            """)],
        )
        planner = Agent(
            model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                             api_key=OPENROUTER_API_KEY),
            instructions=["Draft a balanced, day‑by‑day itinerary."],
        )

        with st.spinner("Researching…"):
            research = researcher.run(f"Research {dest} for {days}‑day trip")
        with st.spinner("Planning trip…"):
            plan = planner.run(f"Destination:{dest}\nDays:{days}\nResearch:{research.content}")
        st.markdown(plan.content)
