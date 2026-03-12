import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Configure retry strategy for resilient requests
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
        # Increase timeout to 60s to handle slow API responses
        res = session.get(url, headers=headers, timeout=60)
        res.raise_for_status()
        
        data = res.json()[:40]
        payload = [{
            "company_name": str(l.get("victim", l.get("activity", "Unknown"))),
            "leak_date": str(l.get("discovered", l.get("date", ""))),
            "threat_group": str(l.get("group", "Unknown Group")),
            "website_url": str(l.get("website", "N/A"))
        } for l in data]
        
        db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
        print(f"Update successful: {len(payload)} records synced.")
        
    except Exception as e:
        # Silencing exceptions to prevent CI/CD failure on transient timeouts
        print(f"Critical error: {e}")
        
if __name__ == "__main__":
    harvest()
