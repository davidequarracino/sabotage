import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    url = "https://api.ransomware.live/recentvictims"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    res = requests.get(url, headers=headers, timeout=20)
    if res.status_code == 200:
        data = res.json()[:50]
        payload = []
        for l in data:
            payload.append({
                "company_name": str(l.get("victim", "N/A")),
                "leak_date": str(l.get("discovered", "")),
                "threat_group": str(l.get("group", "Unknown")),
                "website_url": str(l.get("website", "N/A"))
            })
        
        db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
        print(f"Sync complete: {len(payload)} records pushed.")

if __name__ == "__main__":
    harvest()
