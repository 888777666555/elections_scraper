import requests
from bs4 import BeautifulSoup
import csv

url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"

# vytvoreni listu linku na jednotive mesta
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

td_elements = soup.find_all("td", {"class": "center"})
all_links = []
for td in td_elements:
    link = td.find("a")
    if link:
        href = link.get("href")
        full_url = "https://volby.cz/pls/ps2017nss/" + href
        all_links.append(full_url)

# ziskani kazdeho odkazu ze seznamu all_links
every_second_link = all_links[1::2]

village = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table", class_="table")
for table in tables:
    rows = table.find_all("tr")
    for row in rows[2:]:  # Skip the first two rows as they contain headers
        cells = row.find_all("td")

        data = {
            "name": cells[1].text.strip(),
        }
        village.append(data)

# uprava linku, tak aby byly v uvozovkach
every_second_link_with_quotes = [f"'{link}'" for link in every_second_link]

# zkombinovani nazvu mest a jejich odpovidajici odkazy
village_data = list(zip(village, every_second_link_with_quotes))

# zapsani dat do CSV souboru, kde si uzivatel vybere mesto ktere chce scrapovat
with open("seznam_linku_mest.csv", mode="w", encoding="utf-8", newline="") as file:
    fieldnames = ["name", "links"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for data, link in village_data:
        writer.writerow({"name": data["name"], "links": link})

print("Výstupní soubor CSV obsahujíci všechny linky byl vytvořen. Mužete vybrat město")
