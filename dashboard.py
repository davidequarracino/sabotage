import streamlit as st
import os
from supabase import create_client

# Page config
st.set_page_config(page_title="sabotage | Intelligence Dashboard", layout="wide")
st.title("🕵️ sabotage - Ransomware Feed")

# Initialize connection
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_connection()

# Fetch data
def fetch_data():
    res = supabase.table("cyber_leaks").select("*").order("created_at", desc=True).execute()
    return res.data

data = fetch_data()

if data:
    # Stats
    st.metric("Total Incidents", len(data))
    
    # Data Table
    st.dataframe(
        data, 
        column_config={
            "website_url": st.column_config.LinkColumn("Evidence Link"),
            "created_at": st.column_config.DatetimeColumn("Ingestion Date")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No data available in the pipeline.")
