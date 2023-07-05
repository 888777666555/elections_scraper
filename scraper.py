import sys
import requests
import csv
from bs4 import BeautifulSoup


# funkce pro kontrolu podminek, argumentu
def podminky():
    # Zkontrolujte, zda je uveden správný počet argumentů
    if len(sys.argv) != 3:
        print(
            "Pro spuštění chybí argument, argument1: 'URL' a argument2: 'JMENO SOUBORU'",
            "Zapište: python scraper.py 'URL' 'JMENO SOUBORU'",
        )
        quit()
    url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2109"
    user_url = sys.argv[1]
    filename = sys.argv[2]
    response = requests.get(url)
    user_response = requests.get(user_url)

    # Porovna obsah odpovědí
    if response.status_code == 200 and user_response.status_code == 200:
        if response.text == user_response.text:
            print("odkaz na stranku je v poradku")
        # elif user_url != sys.argv[1]:
        #     print('Url odkaz musi byt uveden jako prvni argument')
        else:
            print("nespravny odkaz na stranku.")
            quit()
    else:
        print("Chyba: Nepodarilo se nacist data z jedne nebo obou adres URL")

    # Zkontrolujte, zda je zadán správný název souboru
    if filename != "vysledky_praha_vychod.csv":
        print("Nezadal jste ale správné jméno souboru.")
        quit()


podminky()


# funkce pro overeni, pro prehled argumentu
def prehled():
    print("Jméno spuštěného programu je:", sys.argv[0])
    print("Jméno Url je:", sys.argv[1])
    print("Jméno souboru je:", sys.argv[2])


prehled()


# odkaz na web stranku voleb do poslanecke snemovny
url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2109"


# funkce vraci odkazy
def ziskej_prvni_odkazy(url) -> list:
    """
    Popis: funkce vraci odkazy na jendotlive obce

    Priklad: 'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=538043&xvyber=2109'

    Vysledek:['https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=538043&xvyber=2109']
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    first_links = []
    td_elements = soup.find_all("td", {"class": "cislo"})
    for td in td_elements:
        link = td.find("a")
        if link:
            href = link.get("href")
            full_url = "https://volby.cz/pls/ps2017nss/" + href
            first_links.append(full_url)

    return first_links


# funkce parsuje hodnoty z odkazu
def ziskej_informace_odkazu(odkaz) -> list:
    """
    Popis: funkce generuje hodnoty obce, konkrente registered, envelopes, valid,
    party names a votes

    Priklad: 289, 214,  213, Občanská demokratická strana, 50

    Vysledek: 289 214 213 [('Občanská demokratická strana', '50')]
    """

    response = requests.get(odkaz)
    soup = BeautifulSoup(response.text, "html.parser")
    registered = soup.find("td", {"headers": "sa2"}).text.strip().replace("\xa0", "")
    envelopes = soup.find("td", {"headers": "sa3"}).text.strip().replace("\xa0", "")
    valid = soup.find("td", {"headers": "sa6"}).text.strip().replace("\xa0", "")
    party_names = soup.find_all(
        "td", {"class": "overflow_name", "headers": "t1sa1 t1sb2"}
    )
    party_votes = soup.find_all("td", {"class": "cislo", "headers": "t1sa2 t1sb3"})
    party_results = []
    for name, votes in zip(party_names, party_votes):
        party_name = name.text.strip().replace("\xa0", "")
        party_vote = votes.text.strip().replace("\xa0", "")
        party_results.append((party_name, party_vote))

    return registered, envelopes, valid, party_results


# funkce parsuje hodnoty, vsech obci
def vsechny_data() -> list:
    """
    Popis: funkce generuje hodnoty z vsech obci, konkrente registered, envelopes, valid,
    party names a votes. Kombinuje vnorene funkce ziskej_prvni_odkazy
    a ziskej_informace_odkazu.

    Priklad: registred: 732, envelops: 533, valid: 531,
    other_information: Občanská demokratická strana : 79

    Vysledek: [{'registred': '732', 'envelops': '533', 'valid': '531',
    'other_information': [('Občanská demokratická strana', '79')]
    """
    all_data = []
    prvni_odkazy = ziskej_prvni_odkazy(url)
    ab = 0
    for odkaz in prvni_odkazy:
        informace = ziskej_informace_odkazu(odkaz)

        a = {
            "registred": informace[0],
            "envelops": informace[1],
            "valid": informace[2],
            "other_information": informace[3],
        }
        ab = ab + 1
        # informace = ziskej_informace_odkazu(odkaz)
        all_data.append(a)
    return all_data


# funkce na vyparsovani mest a kodu
def kod_jmeno() -> list:
    """
    Popis: vyparsovani vsech mest a jejich kodu z voleb do poslanecke snemovny pro Praha-vychod

    Priklad: 538043, Babice

    Vysledek: [{'code': '538043', 'name': 'Babice'}]
    """
    villages = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[2:]:  # Skip the first two rows as they contain headers
            cells = row.find_all("td")

            data = {
                "code": cells[0].text.strip(),
                "name": cells[1].text.strip(),
            }
            villages.append(data)

    return villages


# funkce pro vytvoreni csv  z udaju ktere vraci kod_jmeno a vsechny_data
def zapis_data(main_data: list, another_data: list, jmeno_souboru: str) -> csv:
    """
    Popis:  funkce vytvari csv soubr z voleb do poslanecke snemovny pro Praha-vychod

    Vysledek: vysledky_praha_vychod.csv
    """

    combined_data = []
    all_keys = set()

    # Sbíra všechna jedinečná jména stran
    for data in another_data:
        other_info = data["other_information"]
        party_names = [item[0] for item in other_info]
        all_keys.update(party_names)

    # Převede sadu klíčů na seřazený seznam jednotlivych stran
    sorted_keys = sorted(all_keys)

    for main, another in zip(main_data, another_data):
        row = {
            "code": main["code"],
            "name": main["name"],
            "registred": another["registred"],
            "envelops": another["envelops"],
            "valid": another["valid"],
        }

        # Inicializujte hodnoty pro názvy stran na prázdné řetězce
        for key in sorted_keys:
            row[key] = ""

        # Aktualizujte řádek hodnotami z other_information
        other_info = another["other_information"]
        for item in other_info:
            party_name = item[0]
            party_value = item[1]
            row[party_name] = party_value

        combined_data.append(row)
    # zapise csv
    try:
        with open(jmeno_souboru, mode="w", encoding="utf-8", newline="") as csv_soubor:
            fieldnames = [
                "code",
                "name",
                "registred",
                "envelops",
                "valid",
            ] + sorted_keys
            writer = csv.DictWriter(csv_soubor, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(combined_data)

        return "Saved"
    except Exception as e:
        return str(e)


partai_data = vsechny_data()
code_name_data = kod_jmeno()

vysledek = zapis_data(code_name_data, partai_data, "vysledky_praha_vychod.csv")
print(vysledek)
