import os, streamlit as st, pandas as pd, tempfile, csv, json
from phi.model.openrouter import OpenRouter
from phi.agent.duckdb import DuckDbAgent

# ───────────────────────────────────────────────────────────
REQUIRED_ENV = ["OPENROUTER_API_KEY"]
missing = [v for v in REQUIRED_ENV if not os.getenv(v)]
if missing: st.error(f"Missing env: {', '.join(missing)}"); st.stop()
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
# ───────────────────────────────────────────────────────────

def render_data_analyst():
    st.header("📊 Data‑Analyst Agent")
    file = st.file_uploader("Upload CSV / Excel", type=["csv", "xlsx"])
    query = st.text_area("Ask a question about the data")

    if st.button("Run") and file and query:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            df.to_csv(tmp.name, index=False, quoting=csv.QUOTE_ALL)
            csv_path = tmp.name

        semantic = { "tables": [ { "name": "uploaded", "description": "User file", "path": csv_path } ] }
        duck = DuckDbAgent(
            model = OpenRouter(id="gpt-4o", api_key=OPENROUTER_API_KEY),
            semantic_model = json.dumps(semantic),
            markdown = True,
            followups=False,
        )
        with st.spinner("Running SQL + analysis…"):
            resp = duck.run(query)
        st.markdown(resp.content)
