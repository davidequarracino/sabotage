import streamlit as st
from supabase import create_client

# Page configuration
st.set_page_config(page_title="Sabotage Intelligence", layout="wide")

st.title("Sabotage - Ransomware Incident Feed")

# Secure connection to Supabase via Streamlit Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# Sidebar for intelligence filtering
st.sidebar.header("Data Filtering")
search = st.sidebar.text_input("Search Company or Threat Group")

# Fetch data from Supabase, ordered by most recent leak
# Fetch data from Supabase, ordered by most recent leak
query = supabase.table("cyber_leaks").select("*").order("leak_date", desc=True)
data = query.execute()

if data.data:
    incidents = data.data
    
    # In-memory filtering for responsive UI
    if search:
        incidents = [i for i in incidents if search.lower() in str(i).lower()]

    st.metric("Total Incidents", len(incidents))

    # Link formatting and data cleaning
    for item in incidents:
        link = item.get('evidence_link', '')
        # Only render valid HTTP links to avoid broken UI
        if link and link.startswith('http'):
            item['Evidence'] = link
        else:
            item['Evidence'] = None

    # Professional data display with LinkColumn support
    st.dataframe(
        incidents,
        column_order=("company_name", "leak_date", "threat_group", "Evidence"),
        column_config={
            "company_name": "Target Organization",
            "leak_date": "Discovery Date",
            "threat_group": "Threat Actor",
            "Evidence": st.column_config.LinkColumn("Evidence URL", display_text="External Link")
        },
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No intelligence records found in the database.")
