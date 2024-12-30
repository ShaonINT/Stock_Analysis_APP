from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

import os
from dotenv import load_dotenv
load_dotenv()

# Set API key
Groq.api_key = os.getenv("GROQ_API_KEY")

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
    instructions=["Show the technical indicators including 50 & 200 days moving averages, RSI, Volumn in a figure"],
    show_tool_calls=True,
    markdown=True,
)

# Execute the task
try:
    multi_ai_agent.print_response(
        "Summarise Analyst Recommendations and share latest news for MSTR",
        stream=True
    )
except Exception as e:
    print(f"Error occurred: {e}")