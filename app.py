# app.py – Maarga AI Agent Hub (streamlined)
# ---------------------------------------------------------------
# • Music Generator and Video Analyst tabs removed
# • No top header/logo; sidebar logo enlarged
# • Selected agent name highlighted
# • Keys still checked at startup

import os, streamlit as st

# ── Fail fast if no LLM key ─────────────────────────────────────
if not (os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")):
    st.error("Missing OPENAI_API_KEY or OPENROUTER_API_KEY in environment (.env).")
    st.stop()

# ── Import each agent’s render function ─────────────────────────
from Data_Analyst_Agent.data_analyst_ui           import render_data_analyst
from AI_Travel_Planner.travel_planner_ui          import render_travel_planner
from BreakUp_Recovery_Agent.breakup_recovery_ui   import render_breakup_recovery
from ai_medical_imaging_agent.medical_imaging_ui  import render_medical_imaging
from AI_Data_Visualisation_Agent.data_visualisation_ui import render_data_visualisation
from ai_startup_trend_analysis_agent.startup_trend_ui  import render_startup_trend
from xai_finance_agent.finance_ui                 import render_finance
from opeani_research_agent.research_ui            import render_openai_research
from ai_blog_to_podcast_agent.blog_to_podcast_ui  import render_blog_to_podcast
from multimodal_ai_agent_image.image_reasoner_ui  import render_image_reasoner

# ── Sidebar vertical navigation  ───────────────────────────────
AGENT_NAMES = [
    "📊 Data Analyst",
    "✈️ Travel Planner",
    "💔 Break‑up Recovery",
    "🩺 Medical Imaging",
    "📈 Data‑Vis Agent",
    "🚀 Startup Trend",
    "💹 Finance Agent",
    "📰 Research Agent",
    "🎙️ Blog → Podcast",
    "🧠 Image Reasoner",
]

# Use a more robust way to handle the logo path
try:
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maarga_logo.png")
    if not os.path.exists(logo_path):
        # Try lowercase extension as fallback
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "maarga_logo.PNG")
except Exception as e:
    st.warning("Logo file not found. The application will continue without the logo.")
    logo_path = None

with st.sidebar:
    if logo_path and os.path.exists(logo_path):
        st.image(logo_path, width=200)  # larger logo
    st.header("🗂️ Maarga Agents")
    selected = st.radio("Choose an agent", AGENT_NAMES, key="agent_selector")
    st.markdown("---")
    st.caption("Scroll if list overflows")

# ── Highlight selected agent name in main area ─────────────────
selected_clean = selected.split(" ", 1)[1] if " " in selected else selected
st.markdown(f"## **{selected_clean}**")

# ── Render the selected agent ──────────────────────────────────
if selected == AGENT_NAMES[0]:
    render_data_analyst()
elif selected == AGENT_NAMES[1]:
    render_travel_planner()
elif selected == AGENT_NAMES[2]:
    render_breakup_recovery()
elif selected == AGENT_NAMES[3]:
    render_medical_imaging()
elif selected == AGENT_NAMES[4]:
    render_data_visualisation()
elif selected == AGENT_NAMES[5]:
    render_startup_trend()
elif selected == AGENT_NAMES[6]:
    render_finance()
elif selected == AGENT_NAMES[7]:
    render_openai_research()
elif selected == AGENT_NAMES[8]:
    render_blog_to_podcast()
elif selected == AGENT_NAMES[9]:
    render_image_reasoner()
