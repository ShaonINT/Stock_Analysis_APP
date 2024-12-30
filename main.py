from flask import Flask, request, render_template
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
from dotenv import load_dotenv
import io
import sys
import re

# Load environment variables
load_dotenv()

# Set API key
Groq.api_key = os.getenv("GROQ_API_KEY")

# Define Agents
websearch_agent = Agent(
    name="Web Search Agent",
    role="Search for latest news",
    model=Groq(id="gemma2-9b-it"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources in the response."],
    show_tool_calls=False,
    add_history_to_messages=False,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="gemma2-9b-it"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_news=True)],
    instructions=["Provide stock fundamentals, key ratings, and price targets."],
    show_tool_calls=False,
    add_history_to_messages=False,
    markdown=True,
)

multi_ai_agent = Agent(
    team=[websearch_agent, finance_agent],
    model=Groq(id="gemma2-9b-it"),
    instructions=[
        "Summarize stock data.",
        "Include analyst ratings, top news highlights, and price targets.",
    ],
    show_tool_calls=False,
    markdown=True,
)

# Flask app setup
app = Flask(__name__)

# Function to clean terminal color codes
def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text).strip()

# Home route
@app.route('/')
def home():
    return render_template('index.html')  # Render the HTML file for the user interface

# Route for stock analysis
@app.route('/analyze', methods=['POST'])
def analyze():
    stock_symbol = request.form.get('stock_symbol')
    if not stock_symbol:
        return render_template('index.html', error="Please provide a stock symbol!")

    try:
        # Redirect stdout to capture print output
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Execute task with a short prompt
        multi_ai_agent.print_response(
            f"Summarize stock performance for {stock_symbol} including ratings, news highlights, and price targets.",
            stream=False
        )

        # Restore stdout
        sys.stdout = old_stdout

        # Capture and clean the output
        response = new_stdout.getvalue().strip()
        clean_response = strip_ansi_codes(response)

        # Debugging: Log clean response to ensure correctness
        print(f"Clean Response: {clean_response}")

        # If the response is empty or irrelevant
        if not clean_response or "No relevant" in clean_response:
            clean_response = "No relevant information found. Please try a different stock symbol."

        return render_template('index.html', response=clean_response)
    except Exception as e:
        sys.stdout = old_stdout
        return render_template('index.html', error=f"An error occurred: {str(e)}")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)