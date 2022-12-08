import os
import json
import requests
from bs4 import BeautifulSoup

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

def scraping_pages(object):
    print("Proses scraping dimulai...")
    page = 1
    i = 1
    while page != 70:
        url = f"https://www.carsome.id/beli-mobil-bekas?pageNo={page}"
        pages = requests.get(url)
        soup = BeautifulSoup(pages.text, 'html.parser')
        cars = soup.find_all('article', 'mod-card')
        for item in cars:
            # Title
            listing = item.find('a', 'mod-card__title').text.strip()

            # ID
            id = i
            
            # Year
            tahun = int(listing.split()[0])

            # Manufacturer
            manufacturer = listing.split()[1]

            # Name
            nama = listing.split()[2].capitalize()

            # Odo
            detail = item.find('div', 'mod-card__car-other').text.strip()
            km = int(detail.split()[0].replace('.', ''))

            # Transmission
            transmisi = detail.split()[2]

            # Harga
            harga = int(item.find('strong').text.strip().replace('.', ''))

            result = {
                "id": id,
                "perusahaan": manufacturer,
                "nama_mobil": nama,
                "tahun": tahun,
                "odo": km,
                "jenis_transmisi": transmisi,
                "harga": harga
            }
            i += 1
            object.append(result)

        page += 1
    print("Proses scraping selesai")

def main():
    records = []
    scraping_pages(records)
    dump = json.dumps(records, indent=4)
    with open("./data/data_mobil.json", "w") as file:
        file.write(dump)
        file.close()

main()