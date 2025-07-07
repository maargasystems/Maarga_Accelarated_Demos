import os, streamlit as st
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.models.openai import OpenAIChat

REQUIRED_ENV=["OPENROUTER_API_KEY"]; 
if not os.getenv("OPENROUTER_API_KEY"): st.error("OPENROUTER_API_KEY missing"); st.stop()
API_KEY=os.environ["OPENROUTER_API_KEY"]

def render_startup_trend():
    st.header("🚀 Startup Trend Analysis")
    topic = st.text_input("Startup topic")
    if st.button("Analyze") and topic:
        search = Agent(model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                                        api_key=API_KEY),
                       tools=[DuckDuckGoTools(search=True,news=True,fixed_max_results=5)],
                       instructions=["Gather recent news links about the topic"],
                       markdown=True)
        summar = Agent(model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                                        api_key=API_KEY),
                       tools=[Newspaper4kTools(read_article=True,include_summary=True)],
                       instructions=["Summarise the articles"], markdown=True)
        trend  = Agent(model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                                        api_key=API_KEY),
                       instructions=["Highlight emerging trends & opportunities"],
                       markdown=True)
        with st.spinner("Searching…"):
            links = search.run(topic).content
        with st.spinner("Summarising…"):
            sums  = summar.run(links).content
        with st.spinner("Analyzing trends…"):
            report = trend.run(sums).content
        st.markdown(report)
