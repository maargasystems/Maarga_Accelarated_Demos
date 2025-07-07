def render_multimodal_video():
    import os, tempfile, pathlib, streamlit as st
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
    from agno.media import Video

    OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_KEY:
        st.error("Missing OPENROUTER_API_KEY in environment (.env)")
        st.stop()

    st.header("🧬 Multimodal Video Analyst")

    uploaded = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"], key="video_upload")
    question  = st.text_area("Ask a question about the video",
                             "Summarise the main events and estimate the mood of the scene.")

    with st.expander("What can I ask?"):
        st.markdown("""
* “Describe the main actions in this clip.”  
* “What objects or logos are visible?”  
* “Generate a 3‑sentence summary.”  
* “Is this suitable for children under 10?”  
        """)

    if st.button("Analyze", key="video_analyze_button") and uploaded and question.strip():
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tmp.write(uploaded.read())
        tmp.close()

        video_obj = Video(filepath=tmp.name)

        agent = Agent(
            name="VideoAnalyst",
            model=OpenAIChat(
                id="openai/gpt-4o",
                base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_KEY,
            ),
            markdown=True,
            instructions=[
                "You are a multimodal analyst. First watch the video frame‑by‑frame.",
                "Identify key objects, people, actions and scene changes.",
                "Then answer the user's question in 2‑4 concise paragraphs.",
                "If the user asks for safety or suitability, include a brief age rating justification.",
            ],
        )

        with st.spinner("Processing video… this may take a minute"):
            try:
                run_response = agent.run(
                    f"First analyse the video thoroughly, then answer: {question}",
                    videos=[video_obj],
                )
            except Exception as e:
                st.error(f"Agent call failed: {e}")
                pathlib.Path(tmp.name).unlink(missing_ok=True)
                st.stop()

        st.video(tmp.name)
        st.markdown(run_response.content)
        pathlib.Path(tmp.name).unlink(missing_ok=True)
