import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key
Groq.api_key = os.getenv("GROQ_API_KEY")

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define Agents
# Websearch Agent
websearch_agent = Agent(
    name="Web Search Agent",
    role="Search the websites for latest news",
    model=Groq(id="llama-3.1-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include Sources"],
    show_tool_calls=True,
    add_history_to_messages=True,
    markdown=True,
)

# Financial Agent
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.1-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
                         stock_fundamentals=True, company_news=True, technical_indicators=True)],
    instructions=["Use tables to display data", "Show price Target of 2025 - 2030 in a table"],
    show_tool_calls=True,
    add_history_to_messages=True,
    markdown=True,
)

# Multi-Agent System
multi_ai_agent = Agent(
    team=[websearch_agent, finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Show the technical indicators including 50 & 200 days moving averages, RSI, Volume in a figure"],
    show_tool_calls=True,
    markdown=True,
)


# Streamlit App Interface
st.title("AI-Driven Stock Analysis")
st.write("Enter a stock symbol to get the latest news and analyst recommendations.")

# User Input
stock_symbol = st.text_input("Stock Symbol", placeholder="e.g., MSTR")

if st.button("Analyze"):
    if stock_symbol:  # Check if the user provided a stock symbol
        with st.spinner(f"Fetching data for {stock_symbol}..."):
            try:
                # Execute the task
                response = multi_ai_agent.print_response(
                    f"Summarize Analyst Recommendations and share latest news for {stock_symbol}",
                    stream=False  # Ensure streaming doesn't interfere with the app
                )

                # Debugging: Log raw response
                logging.info(f"Raw response: {response}")
                st.write("Raw Response:", response)  # Display raw response for debugging

                # Display formatted response to the user
                if response:
                    if isinstance(response, dict):  # If the response is a dictionary
                        st.json(response)  # Display as JSON
                    elif isinstance(response, str):  # If the response is Markdown-compatible
                        st.markdown(response)
                    else:  # Fallback for unknown response types
                        st.write(response)

                    # Example: Display structured data as a table if present
                    if isinstance(response, dict) and "table_data" in response:
                        import pandas as pd
                        st.table(pd.DataFrame(response["table_data"]))

                else:
                    st.warning("No data received from the agent. Please try again.")

            except Exception as e:
                # Log the error and display to the user
                logging.error(f"Error while processing {stock_symbol}: {e}")
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a stock symbol!")

# Instructions for Running
st.write("**Instructions:**")
st.write("Run the app using the following command in your terminal:")
st.code("streamlit run app.py", language="bash")