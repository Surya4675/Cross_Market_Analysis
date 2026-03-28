# 📊 Cross Market Analysis Dashboard

## 📖 Overview
The **Cross Market Analysis Dashboard** is a powerful, interactive web application built with Streamlit and SQLite. It provides users with a comprehensive view of historical trends and correlations across multiple financial domains: **Cryptocurrency**, **Oil Markets**, and **Traditional Stock Indices** (S&P 500, NASDAQ, NIFTY). 

By bringing together data from disparate asset classes into a unified relational database, this dashboard enables seamless cross-market comparative analysis, financial tracking, and data exploration.

## ✨ Features

- **Filters & Data Exploration:** 
  - Dynamic date inputs to query market data for specific timeframes.
  - KPI metric cards tracking average Bitcoin, Oil, S&P 500, and NIFTY prices across the selected period.
  - A comprehensive "Daily Market Snapshot" table that joins multi-source data by date.

- **SQL Query Runner:**
  - Execute pre-loaded, complex SQL queries directly from the UI.
  - Queries are logically grouped into categories: **Crypto**, **Crypto Prices**, **Oil**, **Stock Indices**, and **Cross-Market Joins**.
  - Supports quick analytics like *Bitcoin vs Oil trends*, *Top Coin Averages*, *Stock Volatility*, and more.

- **Top 3 Crypto Analysis:**
  - Deep dive into the market's leading cryptocurrencies (Bitcoin, Ethereum, Tether).
  - Clean, interactive line charts tracking price movements (`price_inr`) over user-defined date ranges.

## 🏗️ Project Structure
```text
Cross_Market_Analysis/
├── app.py                     # Main Streamlit application and UI logic
├── market.db                  # Local SQLite Database containing all market tables
├── README.md                  # Project documentation
└── Data Files (CSV)           # Raw data sources (potentially used for populating DB):
    ├── cryptocurrencies.csv
    ├── oil_prices.csv
    ├── stock_prices.csv
    └── top3_crypto_prices.csv
```

### Database Schema (market.db)
The backend is powered by a relational SQLite database with the following core tables:
- `crypto_prices` - Time-series data of cryptocurrency prices (e.g., Bitcoin, Ethereum).
- `oil_prices` - Time-series data reflecting historical daily oil prices.
- `stock_prices` - Historical daily data (open, high, low, close) for indices like ^GSPC (S&P 500), ^IXIC (NASDAQ), and ^NSEI (NIFTY).
- `cryptocurrencies` - Metadata, market cap, ATH (All-Time High), and volume data for specific coins.

## 🛠️ Technology Stack
- **Python 3.x**: Core programming language.
- **Streamlit**: Fast, interactive frontend framework for data applications.
- **SQLite3**: Lightweight, disk-based relational database.
- **Pandas**: Data manipulation, filtering, and seamless SQL-to-Dataframe operations.

## 🚀 Installation & Setup

1. **Clone or Download the Repository:**
   Ensure you have the entire `Cross_Market_Analysis` directory on your local machine.

2. **Install Required Libraries:**
   Make sure you have Python installed, then install the required packages:
   ```bash
   pip install streamlit pandas
   ```

3. **Run the Application:**
   Navigate to the project directory in your terminal and execute the Streamlit run command:
   ```bash
   cd path/to/Cross_Market_Analysis
   streamlit run app.py
   ```

4. **Access the Dashboard:**
   Streamlit will automatically open the app in your default web browser (typically at `http://localhost:8501`).

## 💻 Usage & Navigation
Use the **Sidebar** to navigate between the three main views:
1. Go to **Filters & Data Exploration** to get an immediate, high-level overview of a specific date segment.
2. Go to **SQL Query Runner** to dig deep into database statistics. Choose a category and a specific query to render the resulting dataframe.
3. Go to **Top 3 Crypto Analysis** to chart historical trends visually for specific top-tier coins.
