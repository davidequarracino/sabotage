import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    
    # Endpoint ufficiale aggiornato
    url = "https://api.ransomware.live/recentvictims"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) CyberIntelligence/1.0'}
    
    print(f"Scaricando intelligence da: {url}")
    res = requests.get(url, headers=headers, timeout=20)
    
    try:
        # Tenta di leggere il JSON
        data = res.json()[:30] 
        payload = []
        
        for l in data:
            payload.append({
                # L'API usa chiavi diverse a seconda della versione, qui le intercettiamo tutte
                "company_name": str(l.get("post_title", l.get("victim", "Sconosciuto"))),
                "leak_date": str(l.get("published", l.get("discovered", ""))),
                "threat_group": str(l.get("group_name", l.get("group", "Sconosciuto"))),
                "website_url": str(l.get("website", "N/A"))
            })
            
        print("Invio dati a Supabase in corso...")
        db.table("cyber_leaks").upsert(payload, on_conflict="website_url").execute()
        print(f"VITTORIA! Sincronizzati {len(payload)} incidenti reali.")
        
    except Exception as e:
        print(f"L'API non ha restituito dati validi. Errore: {e}")
        print(f"Risposta grezza dal server: {res.text[:200]}") # Ci mostra cosa ha risposto davvero il sito

if __name__ == "__main__":
    harvest()
