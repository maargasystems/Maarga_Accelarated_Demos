import os, streamlit as st, pandas as pd, base64
from io import BytesIO
from PIL import Image
from e2b_code_interpreter import Sandbox
from openai import OpenAI
import re, contextlib, io, sys

REQUIRED_ENV = ["OPENROUTER_API_KEY", "E2B_API_KEY"]
miss=[v for v in REQUIRED_ENV if not os.getenv(v)]
if miss: st.error(f"Missing env: {', '.join(miss)}"); st.stop()
OPENAI_API_KEY = os.environ["OPENROUTER_API_KEY"]
E2B_API_KEY    = os.environ["E2B_API_KEY"]

pattern=re.compile(r"```python\n(.*?)\n```", re.DOTALL)

def _run_code(sb:Sandbox, code:str):
    stdout, stderr = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec = sb.run_code(code)
    if exec.error: return None
    return exec.results

def render_data_visualisation():
    st.header("📈 Data‑Visualisation Agent")
    up = st.file_uploader("Upload CSV", type="csv")
    if up:
        df = pd.read_csv(up)
        st.dataframe(df.head())
        q  = st.text_area("Ask about the data",
             "Compare average cost for two people between categories")
        if st.button("Run query"):
            with Sandbox(api_key=E2B_API_KEY) as sb:
                sb.files.write("file.csv", up)
                client = OpenAI(base_url="https://openrouter.ai/api/v1",
                                api_key=OPENAI_API_KEY)
                resp = client.chat.completions.create(
                    model="deepseek/deepseek-chat-v3-0324:free",
                    messages=[{"role":"system",
                               "content":"You're a data scientist."},
                              {"role":"user","content":q}])
                code=pattern.search(resp.choices[0].message.content or "")
                if code:
                    res=_run_code(sb, code.group(1))
                    if res:
                        for r in res:
                            if hasattr(r,"png") and r.png:
                                img=Image.open(BytesIO(base64.b64decode(r.png)))
                                st.image(img)
                            elif hasattr(r,"figure"):
                                st.pyplot(r.figure)
                            elif isinstance(r,(pd.DataFrame,pd.Series)):
                                st.dataframe(r)
                            else:
                                st.write(r)
                st.write(resp.choices[0].message.content)
