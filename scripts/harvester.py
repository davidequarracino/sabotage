import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
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

        unique_leaks = {}
        for l in raw_data:
            site = l.get("website", "N/A")
            if site not in unique_leaks and site != "N/A":
                unique_leaks[site] = {
                    "company_name": str(l.get("victim", l.get("post_title", l.get("website", "Unknown Victim")))),
                    "leak_date": str(l.get("discovered", l.get("published", l.get("date", "")))),
                    "threat_group": str(l.get("group", "Unknown Group")),
                    "website_url": site,
                    "evidence_url": str(l.get("screenshot", ""))
                }

        payload = list(unique_leaks.values())[:50]
        
        if payload:
            db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
            print(f"Successfully synced {len(payload)} unique records.")

    except Exception as e:
        print(f"Error during harvest: {e}")

if __name__ == "__main__":
    harvest()
