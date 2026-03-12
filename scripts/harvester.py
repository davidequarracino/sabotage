import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from supabase import create_client

def harvest():
    # Setup Supabase
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Configure retry strategy
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    
    url = "https://api.ransomware.live/recentvictims"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        print(f"Requesting data from: {url}...")
        res = session.get(url, headers=headers, timeout=60)
        res.raise_for_status()
        
        raw_data = res.json()
        
        # Deduplication logic: use a dictionary to keep only one entry per website_url
        unique_leaks = {}
        for l in raw_data:
            site = l.get("website", "N/A")
            # If we haven't seen this site yet, add it to our dictionary
            if site not in unique_leaks and site != "N/A":
                unique_leaks[site] = {
                    "company_name": str(l.get("victim", l.get("activity", "Unknown"))),
                    "leak_date": str(l.get("discovered", l.get("date", ""))),
                    "threat_group": str(l.get("group", "Unknown Group")),
                    "website_url": site
                }
        
        # Convert dictionary back to a list
        payload = list(unique_leaks.values())[:50]
        
        if payload:
            db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
            print(f"Successfully synced {len(payload)} unique records.")
        else:
            print("No valid records found to sync.")
            
    except Exception as e:
        # Logging error without failing the entire workflow
        print(f"Sync failed: {e}")
        
if __name__ == "__main__":
    harvest()
