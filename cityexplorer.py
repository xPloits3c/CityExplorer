import pycountry
import pytz
import datetime
import geonamescache
from colorama import init, Fore, Style
import json
import csv

init(autoreset=True)
gc = geonamescache.GeonamesCache()

def menu():
    print(Fore.CYAN + "===== CityExplorer =====")
    print(Fore.CYAN + "----------V1.0----------")
    print(Fore.CYAN + " -xs3c:25")
    print(Fore.CYAN + " -GitHub: https://github.com/xPloits3c")
    print(Fore.CYAN + "------------------------")
    print("1) Choose a country (e.g. Italy)")
    print("2) Collect all the cities of a country")
    print("3) View time zone of multiple countries")
    print("4) Search cities by coordinates")
    print("5) View top-level domain and subdomains for a country")
    print("0) Exit")
    print("============================")

def scegli_paese():
    paese = input("Enter the name of the country: ").strip()
    country = next((c for c in pycountry.countries if paese.lower() in c.name.lower()), None)
    if not country:
        print(Fore.RED + "Country not found.")
        return None
    print(Fore.GREEN + f"You have selected: {country.name} ({country.alpha_2})")
    return country.alpha_2

def salva_dati(dati, nome_file="citta", formato="json"):
    if formato == "json":
        with open(f"{nome_file}.json", "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=4)
    elif formato == "csv":
        with open(f"{nome_file}.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Nome città"])
            for c in dati:
                writer.writerow([c])
    print(Fore.MAGENTA + f"Data saved in '{nome_file}.{formato}'")

def raccogli_citta(country_code):
    print(Fore.YELLOW + f"Country in {country_code}:")
    cities = [city['name'] for city in gc.get_cities().values() if city['countrycode'] == country_code]
    for city in sorted(cities):
        print(Fore.WHITE + f"- {city}")
    print(Fore.GREEN + f"Total cities found: {len(cities)}")

    salva = input("Do you want to save the list to a file? (y/n): ").strip().lower()
    if salva == "y":
        formato = input("File format (json/csv): ").strip().lower()
        nome = input("File name (without extension): ").strip()
        salva_dati(sorted(cities), nome_file=nome, formato=formato)

def mostra_fusi_orari():
    paesi = input("Enter country names separated by commas (es: ita, india, ru, au, us): ").split(",")
    for paese in paesi:
        paese = paese.strip()
        country = next((c for c in pycountry.countries if paese.lower() in c.name.lower()), None)
        if not country:
            print(Fore.RED + f"Country '{paese}' not found.")
            continue
        timezones = pytz.country_timezones.get(country.alpha_2)
        if not timezones:
            print(Fore.RED + f"No time zone found for {paese}")
            continue
        print(Fore.CYAN + f"Time zones for {paese}:")
        for tz in timezones:
            local_time = datetime.datetime.now(pytz.timezone(tz))
            print(Fore.WHITE + f" - {tz}: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")

def ricerca_coordinate():
    try:
        lat = float(input("Enter latitude: ").strip())
        lon = float(input("Enter the longitude: ").strip())
    except ValueError:
        print(Fore.RED + "Invalid coordinates.")
        return

    cities = gc.get_cities()
    closest_city = None
    min_distance = float('inf')

    def distanza(lat1, lon1, lat2, lon2):
        return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5

    for city in cities.values():
        dist = distanza(lat, lon, float(city['latitude']), float(city['longitude']))
        if dist < min_distance:
            min_distance = dist
            closest_city = city

    if closest_city:
        print(Fore.GREEN + f"Nearest city found: {closest_city['name']} ({closest_city['countrycode']})")
        print(Fore.CYAN + f"Coordinate: {closest_city['latitude']}, {closest_city['longitude']}")
    else:
        print(Fore.RED + "No cities found.")

def visualizza_tld_sottodomini():
    paese = input("Enter the name of the country: ").strip()
    country = next((c for c in pycountry.countries if paese.lower() in c.name.lower()), None)
    if not country:
        print(Fore.RED + "Country not found.")
        return

    tld_mapping = {
        'IT': {
            'tld': '.it',
            'sottodomini': ['.gov.it', '.edu.it', '.org.it', '.net.it', '.com.it']
        },
        'US': {
            'tld': '.us',
            'sottodomini': ['.gov.us', '.edu.us', '.mil.us', '.k12.us']
        },
        'FR': {
            'tld': '.fr',
            'sottodomini': ['.gouv.fr', '.asso.fr', '.com.fr']
        },
        'DE': {
            'tld': '.de',
            'sottodomini': ['.gov.de', '.org.de']
        },
        'IN': {
            'tld': '.in',
            'sottodomini': ['.gov.in', '.nic.in', '.ac.in', '.res.in']
        },
        'JP': {
            'tld': '.jp',
            'sottodomini': ['.go.jp', '.ac.jp', '.co.jp', '.or.jp']
        }
        # Puoi aggiungere altri paesi se vuoi
    }

    info = tld_mapping.get(country.alpha_2)
    if info:
        print(Fore.GREEN + f"Top Level Domain for {country.name}: {info['tld']}")
        print(Fore.CYAN + "Common Subdomains:")
        for sub in info['sottodomini']:
            print(Fore.WHITE + f" - {sub}")
    else:
        print(Fore.YELLOW + f"No information available for {country.name}")

def main():
    while True:
        menu()
        scelta = input("Choose an option: ").strip()
        if scelta == "1":
            scegli_paese()
        elif scelta == "2":
            code = scegli_paese()
            if code:
                raccogli_citta(code)
        elif scelta == "3":
            mostra_fusi_orari()
        elif scelta == "4":
            ricerca_coordinate()
        elif scelta == "5":
            visualizza_tld_sottodomini()
        elif scelta == "0":
            print(Fore.MAGENTA + "Exiting the program.")
            break
        else:
            print(Fore.RED + "Scelta non valida.")

if __name__ == "__main__":
    main()
