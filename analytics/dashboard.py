import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

def load_data():
    conn = sqlite3.connect("feedback.db")
    df = pd.read_sql_query("SELECT * FROM query_log ORDER BY timestamp DESC", conn)
    conn.close()
    return df

st.set_page_config(page_title="Query Analytics", layout="wide")
st.title("Chatbot Query & Sentiment Analytics")

df = load_data()

if df.empty:
    st.warning("No data logged yet.")
else:
    st.dataframe(df)

    sentiment_count = df['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['Sentiment', 'Count']
    fig = px.pie(sentiment_count, names='Sentiment', values='Count', title='Sentiment Distribution')
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.histogram(df, x='timestamp', color='sentiment', title="Query Activity Over Time")
    st.plotly_chart(fig2, use_container_width=True)
