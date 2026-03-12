import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Aggiungiamo un Header per evitare di essere bloccati come bot
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberIntelligenceBot/1.0'}
    
    try:
        response = requests.get("https://api.ransomware.live/leaks", headers=headers, timeout=15)
        
        # Se l'API risponde correttamente (codice 200)
        if response.status_code == 200:
            leaks = response.json()[:30]
            
            payload = [{
                "company_name": l.get("victim", "Unknown"),
                "leak_date": l.get("published", ""),
                "threat_group": l.get("group", "Unknown"),
                "website_url": l.get("website", "N/A")
            } for l in leaks]

            db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
            print(f"Sincronizzati {len(payload)} incidenti.")
        else:
            print(f"L'API ha risposto con errore: {response.status_code}")
            
    except Exception as e:
        print(f"Errore durante la richiesta: {e}")

if __name__ == "__main__":
    harvest()
