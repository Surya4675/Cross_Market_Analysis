import streamlit as st
import sqlite3
import pandas as pd

DB = "market.db"
conn = sqlite3.connect(DB)

st.title("📊 Cross Market Analysis Dashboard")

page = st.sidebar.selectbox(
    "Select Page",
    ["Filters & Data Exploration", "SQL Query Runner", "Top 3 Crypto Analysis"],
)

# PAGE 1
if page == "Filters & Data Exploration":
    st.header("Market Filters & Exploration")

    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    if start_date and end_date:
        btc_avg = pd.read_sql(
            f"""
        SELECT AVG(price_inr) FROM crypto_prices
        WHERE coin_id='bitcoin'
        AND date BETWEEN '{start_date}' AND '{end_date}'
        """,
            conn,
        ).iloc[0, 0]

        oil_avg = pd.read_sql(
            f"""
        SELECT AVG(price_inr) FROM oil_prices
        WHERE date BETWEEN '{start_date}' AND '{end_date}'
        """,
            conn,
        ).iloc[0, 0]

        sp_avg = pd.read_sql(
            f"""
        SELECT AVG(close) FROM stock_prices
        WHERE ticker='^GSPC'
        AND date BETWEEN '{start_date}' AND '{end_date}'
        """,
            conn,
        ).iloc[0, 0]

        nifty_avg = pd.read_sql(
            f"""
        SELECT AVG(close) FROM stock_prices
        WHERE ticker='^NSEI'
        AND date BETWEEN '{start_date}' AND '{end_date}'
        """,
            conn,
        ).iloc[0, 0]

        st.metric("Bitcoin Avg Price (INR)", btc_avg)
        st.metric("Oil Avg Price (INR)", oil_avg)
        st.metric("S&P500 Avg Close", sp_avg)
        st.metric("NIFTY Avg Close", nifty_avg)

        st.subheader("Daily Market Snapshot")

        snapshot_query = f"""
        SELECT 
            c.date AS "Date",
            c.price_inr AS "Bitcoin (INR)",
            o.price_inr AS "Oil (INR)",
            s1.close AS "S&P 500",
            s2.close AS "NIFTY"
        FROM crypto_prices c
        JOIN oil_prices o ON c.date = o.date
        JOIN stock_prices s1 ON c.date = s1.date AND s1.ticker = '^GSPC'
        JOIN stock_prices s2 ON c.date = s2.date AND s2.ticker = '^NSEI'
        WHERE c.coin_id = 'bitcoin'
        AND c.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY c.date DESC
        LIMIT 100
        """

        snapshot_df = pd.read_sql(snapshot_query, conn)

        if snapshot_df.empty:
            st.warning("No data for selected date range")
        else:
            st.dataframe(snapshot_df, width="stretch")


# PAGE 2 (FULL 30 QUERIES)

elif page == "SQL Query Runner":
    st.header("Run SQL Queries")

    query_categories = {
        "Crypto": {
            "Top 3 Cryptocurrencies": "SELECT name, market_cap FROM cryptocurrencies ORDER BY market_cap DESC LIMIT 3",
            "Coins Near ATH": "SELECT name FROM cryptocurrencies WHERE current_price >= 0.9*ath",
            "High Volume Coins": "SELECT name FROM cryptocurrencies WHERE total_volume > 1000000000",
            "Avg Market Rank": "SELECT AVG(market_cap_rank) FROM cryptocurrencies",
            "Recent Coins": "SELECT name,date FROM cryptocurrencies ORDER BY date DESC LIMIT 5",
        },
        "Crypto Prices": {
            "Bitcoin Max": "SELECT MAX(price_inr) FROM crypto_prices WHERE coin_id='bitcoin'",
            "Ethereum Avg": "SELECT AVG(price_inr) FROM crypto_prices WHERE coin_id='ethereum'",
            "Top Coin Avg": "SELECT coin_id,AVG(price_inr) FROM crypto_prices GROUP BY coin_id ORDER BY 2 DESC LIMIT 1",
            "Bitcoin Trend": "SELECT date,price_inr FROM crypto_prices WHERE coin_id='bitcoin'",
            "Bitcoin Change": "SELECT date,price_inr FROM crypto_prices WHERE coin_id='bitcoin'",
        },
        "Oil": {
            "Oil Max": "SELECT MAX(price_inr) FROM oil_prices",
            "Oil Min": "SELECT MIN(price_inr) FROM oil_prices",
            "Oil Avg Year": "SELECT strftime('%Y',date),AVG(price_inr) FROM oil_prices GROUP BY 1",
            "Oil Range": "SELECT MAX(price_inr)-MIN(price_inr) FROM oil_prices",
            "Top Oil Days": "SELECT date,price_inr FROM oil_prices ORDER BY price_inr DESC LIMIT 5",
        },
        "Stock Indices": {
            "NASDAQ Max": "SELECT MAX(close) FROM stock_prices WHERE ticker='^IXIC'",
            "S&P500 Max": "SELECT MAX(close) FROM stock_prices WHERE ticker='^GSPC'",
            "NIFTY Max": "SELECT MAX(close) FROM stock_prices WHERE ticker='^NSEI'",
            "Volatility": "SELECT date,(high-low) FROM stock_prices ORDER BY (high-low) DESC LIMIT 5",
            "Monthly Avg": "SELECT ticker,strftime('%Y-%m',date),AVG(close) FROM stock_prices GROUP BY ticker,2",
        },
        "Cross-Market Joins": {
            "BTC vs Oil": "SELECT c.date,c.price_inr,o.price_inr FROM crypto_prices c JOIN oil_prices o ON c.date=o.date WHERE c.coin_id='bitcoin'",
            "BTC vs S&P": "SELECT c.date,c.price_inr,s.close FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE s.ticker='^GSPC'",
            "BTC vs NIFTY": "SELECT c.date,c.price_inr,s.close FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE s.ticker='^NSEI'",
            "BTC vs NASDAQ": "SELECT c.date,c.price_inr,s.close FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE s.ticker='^IXIC'",
            "ETH vs Oil": "SELECT c.date,c.price_inr,o.price_inr FROM crypto_prices c JOIN oil_prices o ON c.date=o.date WHERE c.coin_id='ethereum'",
            "ETH vs NASDAQ": "SELECT c.date,c.price_inr,s.close FROM crypto_prices c JOIN stock_prices s ON c.date=s.date WHERE s.ticker='^IXIC'",
            "Crypto vs Oil Avg": "SELECT AVG(c.price_inr),AVG(o.price_inr) FROM crypto_prices c JOIN oil_prices o ON c.date=o.date",
            "Crypto vs Stock Avg": "SELECT AVG(c.price_inr),AVG(s.close) FROM crypto_prices c JOIN stock_prices s ON c.date=s.date",
            "Oil vs S&P": "SELECT o.date,o.price_inr,s.close FROM oil_prices o JOIN stock_prices s ON o.date=s.date WHERE s.ticker='^GSPC'",
            "Oil vs NASDAQ": "SELECT o.date,o.price_inr,s.close FROM oil_prices o JOIN stock_prices s ON o.date=s.date WHERE s.ticker='^IXIC'",
        },
    }

    # Creating category dropdown first
    category = st.selectbox("Select Query Category", list(query_categories.keys()))

    # Based on category, second dropdown loads queries
    query_name = st.selectbox("Choose Query", list(query_categories[category].keys()))

    if st.button("Run Query"):
        st.dataframe(pd.read_sql(query_categories[category][query_name], conn))

# PAGE 3
elif page == "Top 3 Crypto Analysis":
    st.header("Top 3 Crypto Price Analysis")

    coin = st.selectbox("Select Cryptocurrency", ["bitcoin", "ethereum", "tether"])

    start_date = st.date_input("Start Date", key="start")
    end_date = st.date_input("End Date", key="end")

    df = pd.read_sql(
        f"""
    SELECT date,price_inr FROM crypto_prices
    WHERE coin_id='{coin}'
    AND date BETWEEN '{start_date}' AND '{end_date}'
    """,
        conn,
    )

    st.dataframe(df)
    
    # Safely draw the graph only if there is data (prevents Altair warnings!)
    if not df.empty:
        df["price_inr"] = pd.to_numeric(df["price_inr"], errors="coerce")
        st.line_chart(df.set_index("date")["price_inr"])
    else:
        st.warning("No data available to graph for this date range.")
