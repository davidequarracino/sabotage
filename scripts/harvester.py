import os
import requests
from supabase import create_client

# Load secure credentials from GitHub environment
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# Initialize the Supabase client
supabase = create_client(url, key)

def test_pipeline():
    print("--- Intelligence Harvester Started ---")
    
    # This is a sample record to verify the connection
    # In the future, this will be replaced by real scraped data
    mock_data = {
        "company_name": "Acme Global Testing",
        "leak_date": "2026-03-12",
        "threat_group": "Alpha-Test-Unit",
        "website_url": "https://example.com/security-alert"
    }

    try:
        # Insert the data into your Supabase 'cyber_leaks' table
        response = supabase.table("cyber_leaks").insert(mock_data).execute()
        print(f"SUCCESS: Data successfully stored for {mock_data['company_name']}")
    except Exception as e:
        print(f"ERROR: Connection failed. Details: {e}")

if __name__ == "__main__":
    test_pipeline()
