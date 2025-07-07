import os, streamlit as st, asyncio
from datetime import datetime
from agents import Agent, Runner, WebSearchTool, function_tool, handoff
from pydantic import BaseModel

REQUIRED_ENV=["OPENAI_API_KEY"]
if not os.getenv("OPENAI_API_KEY"): st.error("OPENAI_API_KEY missing"); st.stop()
KEY=os.environ["OPENAI_API_KEY"]

class Plan(BaseModel):
    topic:str; search_queries:list[str]; focus_areas:list[str]
class Report(BaseModel):
    title:str; report:str; sources:list[str]

@function_tool
def save_fact(fact:str, source:str=None)->str:
    if "facts" not in st.session_state: st.session_state.facts=[]
    st.session_state.facts.append({"fact":fact,"src":source or "n/a",
                                   "ts":datetime.now().strftime("%H:%M:%S")})
    return "Saved."

def _agents():
    research=Agent("Research", tools=[WebSearchTool(),save_fact],
      instructions="Summarise web results in ≤300 words.", model="gpt-4o-mini")
    editor  =Agent("Editor", output_type=Report,
      instructions="Write full markdown report (≥1000 words).",
      model="gpt-4o-mini")
    triage  =Agent("Triage", output_type=Plan,
      instructions="Make plan, then handoff to research & editor.",
      handoffs=[handoff(research), handoff(editor)], model="gpt-4o-mini")
    return triage, research, editor

def render_openai_research():
    st.header("📰 OpenAI Researcher")
    topic=st.text_input("Topic")
    if st.button("Start") and topic:
        triage,_,_=_agents()
        async def flow():
            res = await Runner.run(triage,
                     f"Research this thoroughly: {topic}")
            st.markdown("## Report")
            st.markdown(res.final_output if isinstance(res.final_output, str) else res.final_output.report)
        asyncio.run(flow())
