import requests
from bs4 import BeautifulSoup
import datetime

def fetch_soup(station_id):
    dt_obj = datetime.datetime.now()
    dt_date = dt_obj.strftime("%d%m%Y%H%M")
    dt_time = f"{dt_obj.strftime('%H')}%3A{dt_obj.strftime('%M')}"
    url = f"https://bilkom.pl/stacje/tablica?stacja={station_id}&data={dt_date}&time={dt_time}&przyjazd=false&_csrf"
    response = requests.get(url)

    # Check that it worked
    if response.status_code == 200:
        html = response.text
    else:
        print("Failed to fetch page:", response.status_code)

    return BeautifulSoup(html, "lxml")

def parse_soup(soup):
    data = soup.find_all("li", class_="el")[:2]
    elements = soup.select(".timeTableRow")
    entries = []

    for el in elements:
        processed = {}
        processed['train_no'] = el.select_one(".mobile-carrier").text.strip()
        processed['unix_time'] = el.select_one(".date-time-hidden").text.strip()
        processed['time'] = el.select_one(".time").text.strip()
        processed['delay'] = el.select_one(".time").get("data-difference")
        processed['direction'] = el.select_one(".direction").text.strip()
        try:
            processed['platform'] = el.select_one(".track").text.split("/")
        except:
            processed['platform'] = None
        entries.append(processed)

    return entries

for i in parse_soup(fetch_soup("5100579")):
    print(i)

# todo: take into account passing trains (predicting at next station)