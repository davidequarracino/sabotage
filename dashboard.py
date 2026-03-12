import streamlit as st
from supabase import create_client
import pandas as pd

st.set_page_config(page_title="Sabotage Intelligence", layout="wide")
st.title("Sabotage - Ransomware Incident Feed")

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Fetch dati
data_req = supabase.table("cyber_leaks").select("*").order("leak_date", desc=True).execute()

if data_req.data:
    df = pd.DataFrame(data_req.data)
    
    # Sidebar stats
    st.sidebar.metric("Incidents Tracked", len(df))
    search = st.sidebar.text_input("🔍 Search Company or Group")
    
    if search:
        df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]

    # Layout a colonne per Grafico e Top List
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Top Threat Actors")
        top_groups = df['threat_group'].value_counts().head(10)
        st.bar_chart(top_groups)

    with col2:
        st.subheader("Latest Hits")
        st.dataframe(df[['company_name', 'threat_group']].head(10), use_container_width=True)

    # Tabella principale con link
    st.markdown("---")
    st.subheader("All Intelligence Records")
    
    def linkify(url):
        if url and str(url).startswith("http"):
            return f'<a href="{url}" target="_blank">🔗 View Evidence</a>'
        return "N/A"

    cols = ['company_name', 'leak_date', 'threat_group']
    if 'evidence_url' in df.columns:
        cols.append('evidence_url')
        display_df = df[cols].copy()
        display_df['evidence_url'] = display_df['evidence_url'].apply(linkify)
    else:
        display_df = df[cols].copy()
        display_df['evidence_url'] = "Pending Sync..."

    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.info("Database is empty. Run the Harvester Action to fetch data.")
