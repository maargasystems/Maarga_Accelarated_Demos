import os
from uuid import uuid4
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.eleven_labs import ElevenLabsTools
from agno.agent import Agent, RunResponse
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
from firecrawl import FirecrawlApp

# Streamlit Page Setup
st.set_page_config(page_title="📰 ➡️ 🎙️ Blog to Podcast Agent", page_icon="🎙️")
st.title("📰 ➡️ 🎙️ Blog to Podcast Agent")

# Sidebar: API Keys
st.sidebar.header("🔑 API Keys")

openrouter_api_key = st.sidebar.text_input("OpenRouter API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")

# Check if all keys are provided
keys_provided = all([openrouter_api_key, elevenlabs_api_key, firecrawl_api_key])

# Input: Blog URL
url = st.text_input("Enter the Blog URL:", "")

# Button: Generate Podcast
generate_button = st.button("🎙️ Generate Podcast", disabled=not keys_provided)

if not keys_provided:
    st.warning("Please enter all required API keys to enable podcast generation.")

if generate_button:
    if url.strip() == "":
        st.warning("Please enter a blog URL first.")
    else:
        # Set API keys as environment variables for Agno and Tools
        os.environ["OPENAI_API_KEY"] = openrouter_api_key  # Agno uses OPENAI_API_KEY for OpenRouter
        os.environ["ELEVEN_LABS_API_KEY"] = elevenlabs_api_key
        os.environ["FIRECRAWL_API_KEY"] = firecrawl_api_key

        with st.spinner("Processing... Scraping blog, summarizing and generating podcast 🎶"):
            try:
                # 1. Scrape the blog content using Firecrawl
                app = FirecrawlApp(api_key=firecrawl_api_key)
                scraped_data = app.scrape_url(url)
                blog_content = scraped_data.markdown if scraped_data else ""

                if not blog_content:
                    st.error("Could not scrape content from the URL. Please check the URL and try again.")
                    st.stop()
                
                # 2. Create the agent to summarize and convert to audio
                blog_to_podcast_agent = Agent(
                    name="Blog to Podcast Agent",
                    agent_id="blog_to_podcast_agent",
                    model=OpenAIChat(
                        id="gpt-4o",
                        base_url="https://openrouter.ai/api/v1",
                        api_key=openrouter_api_key,
                    ),
                    tools=[
                        ElevenLabsTools(
                            voice_id="JBFqnCBsd6RMkjVDRZzb",
                            model_id="eleven_multilingual_v2",
                            target_directory="audio_generations",
                        ),
                    ],
                    description="You are an AI agent that can summarize text and generate audio using the ElevenLabs API.",
                    instructions=[
                        "When the user provides blog content:",
                        "1. Create a concise summary of the blog content that is NO MORE than 2000 characters long.",
                        "2. The summary should capture the main points while being engaging and conversational.",
                        "3. Use the ElevenLabsTools to convert the summary to audio.",
                        "Ensure the summary is within the 2000 character limit to avoid ElevenLabs API limits.",
                    ],
                    markdown=True,
                    debug_mode=True,
                )

                # 3. Run the agent with the scraped content
                podcast: RunResponse = blog_to_podcast_agent.run(
                    f"Create a podcast from the following blog content:\n\n{blog_content}"
                )

                save_dir = "audio_generations"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio and len(podcast.audio) > 0:
                    filename = f"{save_dir}/podcast_{uuid4()}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio,
                        filename=filename
                    )

                    st.success("Podcast generated successfully! 🎧")
                    audio_bytes = open(filename, "rb").read()
                    st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        label="Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav"
                    )
                else:
                    st.error("No audio was generated. Please try again.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.error(f"Streamlit app error: {e}")
