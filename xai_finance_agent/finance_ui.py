import os, streamlit as st
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

REQUIRED_ENV=["OPENROUTER_API_KEY"]
if not os.getenv("OPENROUTER_API_KEY"): st.error("Need OPENROUTER_API_KEY"); st.stop()
KEY=os.environ["OPENROUTER_API_KEY"]

def render_finance():
    st.header("💹 Finance Agent")
    query = st.text_input("Your finance question")
    if st.button("Run", key="finance_run_button") and query:
        agent = Agent(
            model=OpenRouter(id="x-ai/grok-3-beta", api_key=KEY),
            tools=[
                DuckDuckGoTools(),
                YFinanceTools(stock_price=True, analyst_recommendations=True,
                              stock_fundamentals=True)
            ],
            instructions=["Show numeric data in tables; text in bullets."],
            markdown=True)
        with st.spinner("Crunching numbers…"):
            st.markdown(agent.run(query).content)
