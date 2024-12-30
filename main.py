from flask import Flask, request, jsonify, render_template
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key
Groq.api_key = os.getenv("GROQ_API_KEY")

# Define Agents
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

multi_ai_agent = Agent(
    team=[websearch_agent, finance_agent],
    model=Groq(id="llama-3.1-70b-versatile"),
    instructions=["Show the technical indicators including 50 & 200 days moving averages, RSI, Volume in a figure"],
    show_tool_calls=True,
    markdown=True,
)

# Flask app setup
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML file for the user interface

# Route for stock analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    stock_symbol = request.form.get('stock_symbol')  # Get stock symbol from the form
    if not stock_symbol:
        return jsonify({"error": "Please provide a stock symbol!"})

    try:
        # Capture the response
        response = multi_ai_agent.print_response(
            f"Summarize Analyst Recommendations and share latest news for {stock_symbol}",
            stream=False
        )

        # Return the captured response as JSON
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)