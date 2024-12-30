# AI-Driven Stock Analysis Application

A Flask-based application utilizing PhiData and Groq APIs to analyze stock performance, providing insights such as analyst ratings, price targets, and top news highlights.

<img width="2416" alt="Screenshot 2024-12-30 at 12 20 14" src="https://github.com/user-attachments/assets/87cab25b-a357-48c8-95b4-102a167a3e5f" />


### **📚 Overview**

This project demonstrates the integration of AI agents with financial tools to create a real-world application for stock analysis. It uses the PhiData and Groq APIs to leverage advanced AI models for summarizing financial data and retrieving up-to-date news.

### 🚀 Features

	•	AI-Driven Insights: Summarizes key stock performance indicators like analyst ratings, price targets, and top news.
	•	Groq & PhiData APIs: Seamlessly integrates AI models for data retrieval and processing.
	•	Responsive User Interface: Provides a sleek, mobile-friendly design.
	•	Customizable Agents: Combines AI tools to cater to specific data needs.

### 🌟 How to Set Up

#### Step 1: Clone the Repository

    git clone https://github.com/ShaonINT/Stock_Analysis_APP.git
    cd Stock_Analysis_APP

#### Step 2: Set Up a Virtual Environment

    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate

#### Step 3: Install Dependencies

    pip install -r requirements.txt

#### Step 4: Acquire API Keys

    To use this project, you need to obtain API keys from PhiData and Groq:

##### PhiData API Key

	1.	Sign up at PhiData.
	2.	Navigate to your account dashboard.
	3.	Generate an API key.
	4.	Add it to the .env file as follows:
        PHIDATA_API_KEY=your_phidata_api_key

##### Groq API Key

	1.	Register at Groq Console.
	2.	Subscribe to the required AI models (e.g., llama-3.1-70b-versatile, you can choose any according to your requirements).
	3.	Generate an API key.
	4.	Add it to the .env file as follows:
        GROQ_API_KEY=your_groq_api_key

#### Step 5: Run the Application

    python main.py
    Visit the application in your browser at http://127.0.0.1:5000.

### 📈 How It Works

	1.	Enter a stock symbol (e.g., AAPL) in the input field.
	2.	Click Analyze to retrieve:
	•	Analyst ratings.
	•	Price targets.
	•	Top 3 latest news articles.
	3.	The AI agents use Groq’s models and tools like DuckDuckGo and YFinanceTools to fetch and process the data.

### 🔑 Key Components

	•	Web Search Agent:
	•	Fetches relevant stock-related news using DuckDuckGo.
	•	Finance Agent:
	•	Retrieves financial data such as stock prices, analyst recommendations, and price targets.
	•	Multi-Agent System:
	•	Combines the Web Search Agent and Finance Agent to deliver consolidated results.

### 🛠 Technologies Used

	•	Python: Flask, dotenv
	•	AI Models: Groq API
	•	Web Tools: PhiData, DuckDuckGo, YFinanceTools
	•	HTML/CSS: Responsive design using custom styles.


### 🔗 Resources

	•	PhiData Documentation
	•	Groq Console

