import requests
from bs4 import BeautifulSoup

station_id = "5100579"
url = f"https://bilkom.pl/stacje/tablica?stacja={station_id}&przyjazd=false&_csrf="
response = requests.get(url)

# Check that it worked
if response.status_code == 200:
    html = response.text
else:
    print("Failed to fetch page:", response.status_code)

soup = BeautifulSoup(html, "lxml")

next_train = soup.find_all("li", class_="el")[:2]

print(next_train)

# todo: extract each trains data into the dict
# ! use .select_one()