# import necessary python libraries
from agno.agent import Agent, RunResponse
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.openrouter import OpenRouter
import streamlit as st
 
# --- Streamlit UI ---
st.set_page_config(page_title="Finance Agent", page_icon="💹")
st.title("💹 Finance Agent")
st.caption("Ask finance-related questions and get smart, data-driven answers.")

# Sidebar for API key
st.sidebar.title("API Configuration")
openrouter_api_key = st.sidebar.text_input("Enter your OpenRouter API Key", type="password")
st.sidebar.info("💡 Get your OpenRouter API key from https://openrouter.ai/")
st.sidebar.markdown("[Get OpenRouter API Key](https://openrouter.ai/)")

# Input box
query = st.text_input("Enter your financial question:")

# Run button
if st.button("Run Analysis") and query:
    if not openrouter_api_key:
        st.warning("Please enter your OpenRouter API key in the sidebar.")
    else:
        # create the AI finance agent with the provided API key
        agent = Agent(
            name="Finance Agent",
            model=OpenRouter(id="x-ai/grok-3-beta", api_key=openrouter_api_key),
            tools=[DuckDuckGoTools(), YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
            instructions=["Always use tables to display financial/numerical data. For text data use bullet points and small paragraphs."],
            show_tool_calls=True,
            markdown=True,
        )
        
        with st.spinner("Analyzing..."):
            try:
                response = agent.run(query, stream=False)
                st.markdown(response.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    if not query:
        st.info("Enter your financial question above and click 'Run Analysis' to get started.")
    elif not openrouter_api_key:
        st.info("Please enter your OpenRouter API key in the sidebar to proceed.")