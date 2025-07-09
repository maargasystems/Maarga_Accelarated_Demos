# ai_data_visualisation_agent/data_visualisation_ui.py
"""
Dynamic AI Data‑Visualisation Agent

• Requires OPENROUTER_API_KEY and E2B_API_KEY in environment
• User uploads any CSV and asks a question
• GPT‑4o returns ONE python code block; code is executed in E2B sandbox
• Plots (matplotlib / plotly) and DataFrames are displayed automatically
"""

import os, io, re, base64, contextlib, streamlit as st, pandas as pd
from io import BytesIO
from PIL import Image
from e2b_code_interpreter import Sandbox
from openai import OpenAI

# ── 1. Environment keys ─────────────────────────────────────────
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
E2B_KEY        = os.getenv("E2B_API_KEY")
if not (OPENROUTER_KEY and E2B_KEY):
    st.error("Missing OPENROUTER_API_KEY or E2B_API_KEY in environment.")
    st.stop()

CODE_RE = re.compile(r"```python\s+(.*?)```", re.DOTALL | re.IGNORECASE)

# ── 2. Helper to run code in sandbox ────────────────────────────
def _run_in_sandbox(code: str, csv_bytes: bytes):
    out = []
    with Sandbox(api_key=E2B_KEY) as sb:
        sb.files.write("data.csv", csv_bytes)
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            exec_res = sb.run_code(code)
        if exec_res.error:
            st.error(f"Sandbox error: {exec_res.error}")
        else:
            out = exec_res.results
    return out

# ── 3. Render function (called by main hub) ─────────────────────
def render_data_visualisation():
    st.header("📊 AI Data‑Visualisation Agent")

    # CSV upload
    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    if not uploaded:
        st.info("Please upload a CSV to begin.")
        return

    # Show preview
    st.dataframe(pd.read_csv(uploaded, nrows=5))

    # User query (no default text)
    query = st.text_area("Ask about the data", placeholder="e.g. 'Plot total sales by region'")
    if not query.strip():
        return  # Do nothing until user types something

    if st.button("Run", key="dv_run"):
        # GPT‑4o call
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)
        system_prompt = (
            "You are a senior Python data analyst. A CSV file is saved as 'data.csv'. "
            "Read it into df, normalise column names with "
            "df.columns = df.columns.str.lower().str.strip().str.replace(' ', '_'). "
            "Then answer the user's question by generating a plot or DataFrame. "
            "Return exactly ONE python code block and nothing else (other text may follow)."
        )
        resp = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": query}],
        )
        content = resp.choices[0].message.content or ""
        m = CODE_RE.search(content)
        if not m:
            st.error("Model did not return python code. Raw response:")
            st.markdown(content)
            return

        code = m.group(1)
        st.code(code, language="python")

        # Run code in sandbox
        results = _run_in_sandbox(code, uploaded.getvalue())

        # Render outputs
        for obj in results:
            if hasattr(obj, "png") and obj.png:
                img = Image.open(BytesIO(base64.b64decode(obj.png)))
                st.image(img, use_container_width=True)
            elif hasattr(obj, "figure"):
                st.pyplot(obj.figure)
            elif isinstance(obj, (pd.DataFrame, pd.Series)):
                st.dataframe(obj, use_container_width=True)
            else:
                st.write(obj)

        # Show any summary text after the code block
        summary = CODE_RE.sub("", content).strip()
        if summary:
            st.markdown("---")
            st.markdown(summary)