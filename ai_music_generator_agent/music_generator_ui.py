# ai_music_generator_agent/music_generator_ui.py
"""
Streamlit front‑end for the ModelsLab music‑generation agent.
Keys come only from environment (.env); the UI has no key inputs.
"""

import os, uuid, pathlib, requests, streamlit as st
from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.models_labs import ModelsLabTools, FileType


# ── Utility to verify required env vars ──────────────────────────
def _require_env_vars(names):
    missing = [k for k in names if not os.getenv(k)]
    if missing:
        st.error(f"Missing env vars: {', '.join(missing)}")
        st.stop()


# ── Public entry point called by hub ‑ app.py ───────────────────
def render_music_generator():
    """Render the music‑generator tab in Maarga AI Agent Hub."""
    _require_env_vars(["OPENROUTER_API_KEY", "MODELSLAB_API_KEY"])

    OPENROUTER_KEY = os.environ["OPENROUTER_API_KEY"]
    MODELSLAB_KEY  = os.environ["MODELSLAB_API_KEY"]

    st.header("🎵 AI Music Generator")

    prompt = st.text_area(
        "Describe the music you want",
        "30 s upbeat synth‑pop with catchy bassline and claps",
        height=120,
        key="music_prompt_box",
    )

    with st.expander("Prompt tips"):
        st.markdown(
            """
* **Genre / Style** – EDM, lo‑fi, orchestral …  
* **Instruments** – guitar, synth pads, strings …  
* **Mood / Tempo** – chilled 90 BPM, energetic 128 BPM …  
* **Structure** – intro / verse / chorus …
"""
        )

    if st.button("🎶 Generate", key="music_generate_btn") and prompt.strip():
        agent = Agent(
            name="MusicAgent",
            model=OpenRouter(id="gpt-4o", api_key=OPENROUTER_KEY),
            tools=[
                ModelsLabTools(
                    api_key=MODELSLAB_KEY,
                    wait_for_completion=True,
                    file_type=FileType.MP3,
                )
            ],
            markdown=True,
        )

        with st.spinner("Composing… this can take ~30 s"):
            try:
                run = agent.run(prompt)
            except Exception as e:
                st.error(f"Agent call failed: {e}")
                st.stop()

        if not run.audio:
            st.error("No audio returned. Try a simpler prompt or check API quota.")
            with st.expander("Debug"):
                st.write(run)
            st.stop()

        url = run.audio[0].url
        try:
            audio_bytes = requests.get(url, timeout=30).content
        except Exception as e:
            st.error(f"Download failed: {e}")
            st.stop()

        out_dir = pathlib.Path("audio_generations")
        out_dir.mkdir(exist_ok=True)
        file_path = out_dir / f"music_{uuid.uuid4()}.mp3"
        file_path.write_bytes(audio_bytes)

        st.success("Music generated!")
        st.audio(audio_bytes, format="audio/mp3")
        st.download_button(
            "⬇️ Download MP3",
            audio_bytes,
            file_name="generated_music.mp3",
            mime="audio/mp3",
            key="music_dl_btn",
        )
