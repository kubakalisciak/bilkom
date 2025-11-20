import requests
from bs4 import BeautifulSoup

def fetch_soup(station_id):
    url = f"https://bilkom.pl/stacje/tablica?stacja={station_id}&przyjazd=false&_csrf="
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
        processed['platform'] = el.select_one(".track").text.split("/")
        entries.append(processed)

    return entries[:3]

print(parse_soup(fetch_soup("5100579")))

# ! add delay processing
# todo: take into account passing trains (predicting at next station)
# * fix the bug where on certain stations the platforms are incorectly parsed