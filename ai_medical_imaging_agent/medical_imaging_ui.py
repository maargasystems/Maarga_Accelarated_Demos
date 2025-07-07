import os, streamlit as st
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
from PIL import Image as PIL

REQUIRED_ENV = ["OPENROUTER_API_KEY"]
if not os.getenv("OPENROUTER_API_KEY"): st.error("Need OPENROUTER_API_KEY"); st.stop()
OPENAI_API_KEY = os.environ["OPENROUTER_API_KEY"]

def render_medical_imaging():
    st.header("🩺 Medical Imaging Diagnosis")
    f = st.file_uploader("Upload image", type=["jpg","jpeg","png"])
    if f and st.button("Analyze"):
        img_path = f"tmp_{f.name}"
        open(img_path,'wb').write(f.read())
        agent = Agent(
            model=OpenAIChat(id="gpt-4o", base_url="https://openrouter.ai/api/v1",
                             api_key=OPENAI_API_KEY),
            tools=[DuckDuckGoTools()], markdown=True)
        query = ("You are a radiology expert. Provide modality, findings, "
                 "diagnosis, patient‑friendly explanation, references.")
        with st.spinner("Analyzing…"):
            resp = agent.run(query, images=[AgnoImage(filepath=img_path)])
        st.image(PIL.open(img_path), width=400)
        st.markdown(resp.content)
