import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Chiamata all'API
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get("https://api.ransomware.live/leaks", headers=headers)
    
    if res.status_code == 200:
        data = res.json()[:20]
        payload = []
        for l in data:
            payload.append({
                "company_name": l.get("victim", "N/A"),
                "leak_date": l.get("published", ""),
                "threat_group": l.get("group", "Unknown"),
                "website_url": l.get("website", "")
            })
        
        # Invio dati
        db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
        print("Dati inviati con successo!")

if __name__ == "__main__":
    harvest()
