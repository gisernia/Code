import os
import csv
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

START_YEAR = int(os.getenv("START_YEAR"))
END_YEAR = int(os.getenv("END_YEAR"))
OUTPUT_DETTAGLIO = os.getenv("OUTPUT_DETTAGLIO")
OUTPUT_TOTALI = os.getenv("OUTPUT_TOTALI")
BASE_URL = os.getenv("BASE_URL")
HEADERS = {"User-Agent": os.getenv("HEADERS")}


def scarica_classifica(anno):
    url = BASE_URL.format(start=anno, end=anno)
    print(f"📥 {anno} → {url}")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"   ❌ errore download: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="items")
    if not table or not table.tbody:
        print(f"   ⚠️ classifica non trovata per {anno}")
        return []

    righe = []
    td_rows = table.tbody.find_all("tr")
    tot_squadre = len(td_rows)

    for tr in td_rows:
        td_list = tr.find_all("td")
        if len(td_list) < 9:
            continue

        # posizione
        try:
            posizione = int(td_list[0].text.strip())
        except:
            continue

        # squadra
        squadra_tag = td_list[2].find("a")
        squadra = squadra_tag.text.strip() if squadra_tag else ""

        # punti (ultimo td)
        try:
            punti = int(td_list[-1].text.strip())
        except:
            punti = 0

        righe.append({
            "stagione": anno,
            "squadra": squadra,
            "posizione": posizione,
            "squadre_totali": tot_squadre,
            "punti": punti
        })

    return righe


def salva_csv(file, righe):
    if not righe:
        return
    keys = righe[0].keys()
    with open(file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(righe)


def calcola_totali(tutte_righe):
    totali = defaultdict(int)
    for r in tutte_righe:
        n = r["squadre_totali"]
        punti_stagione = n - r["posizione"] + 1
        totali[r["squadra"]] += punti_stagione
    # ordina per punti decrescente
    lista = sorted(totali.items(), key=lambda x: x[1], reverse=True)
    righe = [{"squadra": s, "punti": p} for s, p in lista]
    return righe


def main():
    tutte_righe = []
    for anno in range(START_YEAR, END_YEAR + 1):
        righe = scarica_classifica(anno)
        tutte_righe.extend(righe)

    # salva dettaglio stagione
    salva_csv(OUTPUT_DETTAGLIO, tutte_righe)
    print(f"✅ salvato dettaglio stagioni in {OUTPUT_DETTAGLIO}")

    # calcola e salva totali
    totali = calcola_totali(tutte_righe)
    salva_csv(OUTPUT_TOTALI, totali)
    print(f"✅ salvato classifica storica cumulativa in {OUTPUT_TOTALI}")


if __name__ == "__main__":
    main()
