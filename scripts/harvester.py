import os, requests
from supabase import create_client

def harvest():
    db = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    url = "https://api.ransomware.live/recentvictims"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    res = requests.get(url, headers=headers)
    print("STATUS CODE:", res.status_code)
    print("PAYLOAD GREZZO (primi 200 char):", res.text[:200])
    
    data = res.json()
    print("NUMERO ELEMENTI RICEVUTI:", len(data))
    
    # Se la lista è vuota, blocchiamo l'esecuzione per vedere l'errore nel log
    assert len(data) > 0, "L'API ha restituito una lista vuota."

if __name__ == "__main__":
    harvest()
