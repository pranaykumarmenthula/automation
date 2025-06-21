import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px


SUPABASE_URL = "https://jwpitflzvgeiuhvlahwq.supabase.co"  
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp3cGl0Zmx6dmdlaXVodmxhaHdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAxNzY2NTksImV4cCI6MjA2NTc1MjY1OX0.8Ik1XOzyRsYn2FAbQD9PtyRnMypU8-g6Pd_rjEfLE1M"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("💸 Personal Expense Tracker")

telegram_id = st.text_input("Enter your Telegram ID").strip()

if st.button("View My Expenses"):
    if not telegram_id:
        st.warning("Please enter your Telegram ID.")
    else:
        try:
            response = supabase.table("user").select("id").ilike("telegram_id", telegram_id).execute()

            if response.data and len(response.data) > 0:
                user_id = response.data[0]["id"]
                st.success(f"Welcome! Your user ID is {user_id}")

                # Fetch expenses
                expense_data = supabase.table("expenses").select("*").eq("user_id", user_id).execute()

                if expense_data.data:
                    df = pd.DataFrame(expense_data.data)
                    st.dataframe(df)

                    # Pie chart by category
                    if "category" in df.columns:
                        fig = px.pie(df, names="category", values="amount", title="Expense Breakdown")
                        st.plotly_chart(fig)
                else:
                    st.info("No expenses found yet.")
            else:
                st.warning("No user found with this Telegram ID.")
        except Exception as e:
            st.error(f"Error: {e}")
