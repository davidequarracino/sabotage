import os, requests
from supabase import create_client

def harvest():
    # Connessione immediata
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Recupero dati reali (Sorgente: Ransomware.live)
    leaks = requests.get("https://api.ransomware.live/leaks", timeout=15).json()[:30]
    
    # Costruzione payload bulk
    payload = [{
        "company_name": l.get("victim", "Unknown"),
        "leak_date": l.get("published", ""),
        "threat_group": l.get("group", "Unknown"),
        "website_url": l.get("website", "N/A")
    } for l in leaks]

    # Invio atomico a Supabase
    db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
    print(f"Sincronizzati {len(payload)} incidenti.")

if __name__ == "__main__":
    harvest()
