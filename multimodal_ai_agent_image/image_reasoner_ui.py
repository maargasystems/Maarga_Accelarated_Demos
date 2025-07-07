import os, streamlit as st, tempfile, pathlib
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.media import Image as AgnoImage

REQUIRED_ENV=["OPENROUTER_API_KEY"]
if not os.getenv("OPENROUTER_API_KEY"): st.error("Need OPENROUTER_API_KEY"); st.stop()
KEY=os.environ["OPENROUTER_API_KEY"]

def render_image_reasoner():
    st.header("🧠 Multimodal Image Reasoner")
    up = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"], key="image_reasoner_upload")
    task = st.text_area("What should I reason about?")
    if st.button("Analyze", key="image_reasoner_analyze_button") and up and task:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(up.read()); tmp.close()
        agent = Agent(model=OpenAIChat(id="google/gemini-2.5-flash-preview-05-20:thinking",
                                       base_url="https://openrouter.ai/api/v1",
                                       api_key=KEY),
                      markdown=True)
        with st.spinner("Thinking…"):
            res = agent.run(task, images=[AgnoImage(filepath=tmp.name)])
        st.image(up); st.markdown(res.content)
        pathlib.Path(tmp.name).unlink(missing_ok=True)
