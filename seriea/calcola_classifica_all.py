import requests
import csv
from bs4 import BeautifulSoup
from time import sleep
from collections import defaultdict

# ==========================
# CONFIGURAZIONE OUTPUT
# ==========================

OUTPUT_TOTALI = "serie_a_totali.csv"
OUTPUT_DETTAGLIO = "serie_a_dettaglio_stagioni.csv"

START_YEAR = 1929   # stagione 1929-30
END_YEAR = 2024     # ultima stagione completa

BASE_URL = "http://calcio-seriea.net"

# ==========================
# STRUTTURE DATI
# ==========================

totali = defaultdict(int)
stagioni_giocate = defaultdict(set)
dettaglio = []

# ==========================
# CICLO STAGIONI
# ==========================

for year in range(START_YEAR, END_YEAR + 1):
    stagione = f"{year}-{str(year+1)[-2:]}"
    url = f"{BASE_URL}/stagione/{stagione}"

    print(f"📥 Scarico stagione {stagione}")

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"   ❌ errore: {e}")
        continue

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table")

    if not table:
        print("   ⚠️ nessuna tabella trovata")
        continue

    rows = table.find_all("tr")
    squadre = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue

        pos = cols[0].get_text(strip=True)
        squadra = cols[1].get_text(strip=True)

        if pos.isdigit():
            squadre.append((int(pos), squadra))

    if not squadre:
        print("   ⚠️ classifica vuota")
        continue

    squadre.sort(key=lambda x: x[0])
    N = len(squadre)

    for posizione, squadra in squadre:
        punti = N - posizione + 1

        totali[squadra] += punti
        stagioni_giocate[squadra].add(stagione)

        dettaglio.append({
            "stagione": stagione,
            "squadra": squadra,
            "posizione": posizione,
            "squadre_totali": N,
            "punti": punti
        })

    sleep(0.5)

# ==========================
# SCRITTURA CSV DETTAGLIO
# ==========================

with open(OUTPUT_DETTAGLIO, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["stagione", "squadra", "posizione", "squadre_totali", "punti"]
    )
    writer.writeheader()
    writer.writerows(dettaglio)

# ==========================
# SCRITTURA CSV TOTALI
# ==========================

ranking = sorted(totali.items(), key=lambda x: x[1], reverse=True)

with open(OUTPUT_TOTALI, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["squadra", "punti_totali", "stagioni"])
    for squadra, punti in ranking:
        writer.writerow([squadra, punti, len(stagioni_giocate[squadra])])

print("\n✅ FATTO")
print(f"📄 creato: {OUTPUT_TOTALI}")
print(f"📄 creato: {OUTPUT_DETTAGLIO}")
