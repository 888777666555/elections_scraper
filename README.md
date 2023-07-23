POPIS PROGRAMU :
Program scraper.py pracuje resp. čte výsledky voleb do poslanecké sněnmovny parlamentu České republiky konané v roku 2017.
Pro projekt jsem vybral volby do poslanecke sněmovny ČR 2017.
Odkaz na web stránku je https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ  
Program čte informace jako je Code -kod obec, Name-nazev obce, Registred-voliči v seznamu, Envelops-vydané obálky, Valid-platné hlasy a pak jednotlivé politické strany a jejích zisk ve volbách pro konkretní obec.
Užívatel si vybere z kterého města chce ziskat informace dle CSV seznam_linku_mest.csv.
Nakonec program zapisuje dané informace do CSV souboru s názvem "vysledky_voleb.csv".

SPUŠTĚNÍ PROGRAMU :
Program je možné spusit v Terminal servru pomoci příkazu:

python scraper.py (konkretni link se seznamu_linku_mest napr. 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100') "vysledky_voleb.csv"

Pro kontrolu správnosti je přidán výpis :
Jméno spuštěného programu je: scraper.py
Jméno Url je: 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100'
Jméno souboru je: "vysledky_voleb.csv"

V případ zadáni nesprávniho příkazu, program užívatele upozorní

KNIHOVNY POUŽITÉ V PROGRAMU:

V programu byly použite zabudované knihovny ale i knihovny třetích strán, které je potřeba před spuštěním programu nainstalované. Je vhodné vytvořit virtuálne prostředí, aby se predešlo komplikacím s prepsánim predešlích verzí knihoven.

Vytvoření virtuálniho prostředí:
prostředí se vytvoří v príkazovem řádku pomoci príkazu : python -m venv moje_prvni_prostredi
následne se musí aktivovat : moje_prvni_prostredi\Scripts\Activate.ps1 - pro Windows nebo
source moje_prvni_prostredi/bin/activate - pro Linux a MacOS.

Zabudované knihovny jsou : sys,csv
Knihovny třetích strán jsou: requests, bs4. Knihovny instaluješ v přikazovém řádku pomoci příkazu : pip install <jmeno_knihovny>

UKÁZKA VÝSTUPNÍHO CSV SOUBORU:
![ctrl + klick na odkaz](image-1.png)
