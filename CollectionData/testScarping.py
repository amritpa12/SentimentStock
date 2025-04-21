import random
import requests
from bs4 import BeautifulSoup

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.9",
}

url = "https://www.tradingview.com/news/zacks:4ac8ee055094b:0-apple-vs-dell-technologies-which-pc-maker-stock-is-a-better-buy/"
response = requests.get(url, headers=headers)
print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

# CNBC typically puts article content in <div class="group"> and <div class="ArticleBody-articleBody">
content_div = soup.find("div", class_="ArticleBody-articleBody")

if content_div:
    paragraphs = content_div.find_all("p")
    article_text = '\n\n'.join(p.get_text() for p in paragraphs)
    print(article_text)
else:
    print("Article content not found.")
