import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="Sabotage Intelligence", layout="wide")
st.title("Sabotage - Ransomware Incident Feed")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

data_req = supabase.table("cyber_leaks").select("*").order("leak_date", desc=True).execute()

if data_req.data:
    df = pd.DataFrame(data_req.data)
    st.sidebar.metric("Total Incidents", len(df))
    search = st.sidebar.text_input("Search Company or Group")
    
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

    def linkify(url):
        if url and str(url).startswith("http"):
            return f'<a href="{url}" target="_blank">🖼️ View Evidence</a>'
        return "N/A"

    display_df = df[['company_name', 'leak_date', 'threat_group', 'evidence_url']].copy()
    display_df['evidence_url'] = display_df['evidence_url'].apply(linkify)
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("No records found.")
