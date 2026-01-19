# Serie A – Classifica storica a punteggio

Script Python che calcola una classifica storica della Serie A (girone unico), scaricando i dati da **Transfermarkt** e assegnando a ogni squadra N punti per il primo posto, N-1 per il secondo, ecc., dove N è il numero di squadre in quella stagione.

## Funzionalità principali

- Scarica automaticamente tutte le stagioni dal **1929 al 2024**.
- Genera un file **dettaglio per stagione** con nome squadra, posizione, numero squadre e punti.
- Calcola una **classifica storica cumulativa** usando lo schema punti N-(posizione-1) per stagione.
- Tutto parametrizzato tramite `.env` per URL, anni e nomi file.

## Output

- `serie_a_dettaglio_stagioni.csv` → dettaglio stagione per stagione  
- `serie_a_totali.csv` → classifica storica cumulativa  

Esempio di dettaglio stagione:

```csv
stagione,squadra,posizione,squadre_totali,punti
1929,Inter Milan,1,18,72
1929,Genoa CFC,2,18,69
1929,Juventus FC,3,18,63
...
```

Esempio di classifica storica cumulativa:

```csv
squadra,punti
Juventus FC,XXXX
Inter Milan,XXXX
AC Milan,XXXX
...
```

## Uso

Dal terminale, dalla cartella `seriea/`:

```bash
python calcola_classifica_all.py
```

## Parametri

I parametri sono parametrizzati tramite il file `.env`:

```env
START_YEAR=1929
END_YEAR=2024
OUTPUT_DETTAGLIO=../serie_a_dettaglio_stagioni.csv
OUTPUT_TOTALI=../serie_a_totali.csv
BASE_URL=https://www.transfermarkt.com/serie-a/ewigeTabelle/wettbewerb/IT1/plus/?saison_id_von={start}&saison_id_bis={end}&tabellenart=alle
HEADERS=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

## DIPENDENZE

```bash
pip install requests beautifulsoup4 python-dotenv
```
