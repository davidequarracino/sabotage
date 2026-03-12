import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    res = requests.get("https://api.ransomware.live/leaks", headers={'User-Agent': 'CyberBot/1.0'})
    res.raise_for_status()
    payload = [{"company_name": str(l.get("victim", "N/A")), "website_url": str(l.get("website", "N/A"))} for l in res.json()[:5]]
    print(db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute())

if __name__ == "__main__":
    harvest()
