import os, streamlit as st, tempfile
from pathlib import Path
from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openai import OpenAIChat

REQUIRED_ENV = ["OPENROUTER_API_KEY"]
if not os.getenv("OPENROUTER_API_KEY"):
    st.error("Missing OPENROUTER_API_KEY"); st.stop()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

def _init_agents():
    model = OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                       api_key=OPENROUTER_API_KEY)
    therapist = Agent(model=model, name="Therapist",
        instructions=["Listen, empathise, comfort."], markdown=True)
    closure   = Agent(model=model, name="Closure",
        instructions=["Write unsent messages for emotional release."], markdown=True)
    planner   = Agent(model=model, name="Routine Planner",
        instructions=["Design 7‑day recovery plan."], markdown=True)
    honesty   = Agent(model=model, name="Brutal Honesty",
        instructions=["Give blunt, objective analysis."],
        tools=[DuckDuckGoTools()], markdown=True)
    return therapist, closure, planner, honesty

def render_breakup_recovery():
    st.header("💔 Break‑up Recovery Squad")
    text = st.text_area("How are you feeling?")
    imgs = st.file_uploader("Chat screenshots (optional)", type=["jpg","png"], accept_multiple_files=True)
    if st.button("Get plan") and (text or imgs):
        th, cl, pl, ho = _init_agents()
        ag_imgs=[]
        for f in imgs:
            p = Path(tempfile.gettempdir())/f.name
            p.write_bytes(f.read())
            ag_imgs.append(AgnoImage(filepath=p))
        with st.spinner("Therapist typing…"):
            st.markdown(th.run(text, images=ag_imgs).content)
        with st.spinner("Writing closure…"):
            st.markdown(cl.run(text, images=ag_imgs).content)
        with st.spinner("Planning routine…"):
            st.markdown(pl.run(text, images=ag_imgs).content)
        with st.spinner("Honest feedback…"):
            st.markdown(ho.run(text, images=ag_imgs).content)
