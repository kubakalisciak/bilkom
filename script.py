import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the page
url = "https://quotes.toscrape.com/"
response = requests.get(url)

# Check that it worked
if response.status_code == 200:
    html = response.text
else:
    print("Failed to fetch page:", response.status_code)

soup = BeautifulSoup(html, "lxml")

# Step 2: Find all quote containers
quotes = soup.find_all("div", class_="quote")

# Step 3: Loop through and print results
for quote in quotes:
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    print(f"{text} — {author}")
