import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # User-Agent necessario per non essere rimbalzati dall'API
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        res = requests.get("https://api.ransomware.live/leaks", headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()[:30]
            payload = []
            for l in data:
                payload.append({
                    "company_name": l.get("victim", "N/A"),
                    "leak_date": l.get("published", ""),
                    "threat_group": l.get("group", "Unknown"),
                    "website_url": l.get("website", "N/A")
                })
            
            # L'upsert ora funzionerà perché la colonna esiste
            db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
            print(f"Sincronizzati {len(payload)} incidenti reali.")
    except Exception as e:
        print(f"Errore: {e}")

if __name__ == "__main__":
    harvest()
