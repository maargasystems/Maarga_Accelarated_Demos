import os, streamlit as st
from agno.agent import Agent, RunResponse
from agno.tools.eleven_labs import ElevenLabsTools
from agno.models.openai import OpenAIChat
from firecrawl import FirecrawlApp
from uuid import uuid4
from agno.utils.audio import write_audio_to_file

# 🔑 required keys
REQUIRED_ENV = ["OPENROUTER_API_KEY", "ELEVENLABS_API_KEY", "FIRECRAWL_API_KEY"]
miss = [v for v in REQUIRED_ENV if not os.getenv(v)]
if miss:
    st.error(f"Missing env vars: {', '.join(miss)}"); st.stop()
OPENROUTER_API_KEY   = os.environ["OPENROUTER_API_KEY"]
ELEVENLABS_API_KEY = os.environ["ELEVENLABS_API_KEY"]
FIRECRAWL_API_KEY  = os.environ["FIRECRAWL_API_KEY"]

def render_blog_to_podcast():
    st.header("🎙️ Blog → Podcast Agent")

    url = st.text_input("Blog URL")
    if st.button("Generate podcast") and url:
        with st.spinner("Scraping + summarising + voicing…"):
            app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
            scraped = app.scrape_url(url)
            if not scraped or not scraped.markdown:
                st.error("Failed to scrape."); return
            blog_md = scraped.markdown[:8000]  # safety

            agent = Agent(
                model=OpenAIChat(
                    id="gpt-4o",
                    base_url="https://openrouter.ai/api/v1",
                    api_key=OPENROUTER_API_KEY),
                tools=[ElevenLabsTools(
                    api_key=ELEVENLABS_API_KEY,
                    voice_id="JBFqnCBsd6RMkjVDRZzb",
                    model_id="eleven_multilingual_v2",
                    target_directory="audio_generations")],
                markdown=True,
            )

            run: RunResponse = agent.run(
                f"Turn this blog into a ≤2000‑char podcast script then call ElevenLabs to voice it:\n\n{blog_md}"
            )
            if run.audio:
                fname = f"audio_generations/podcast_{uuid4()}.wav"
                write_audio_to_file(run.audio[0].base64_audio, fname)
                st.audio(fname, format="audio/wav")
                st.download_button("Download", open(fname, "rb").read(),
                                   file_name="podcast.wav", mime="audio/wav")
            else:
                st.error("No audio returned 😔")
