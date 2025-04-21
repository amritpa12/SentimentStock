
import requests
from newspaper import Article, Config
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_news_newsapi(ticker, api_key, max_articles=20):
    # Configure newspaper3k
    config = Config()
    config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    config.request_timeout = 10
    config.fetch_images = False

    # NewsAPI request
    domains = "reuters.com,bloomberg.com,cnbc.com,finance.yahoo.com,marketwatch.com"  # Prioritize accessible sources
    url = f"https://newsapi.org/v2/everything?q={ticker}+stock&domains={domains}&language=en&sortBy=relevancy&apiKey={api_key}"
    response = requests.get(url)
    articles = []

    if response.status_code != 200:
        print(f"NewsAPI error for {ticker}: {response.status_code} - {response.text}")
        return pd.DataFrame(articles)

    data = response.json()
    for item in data['articles'][:max_articles]:
        time.sleep(1)  # Avoid rate limiting
        try:
            # Try newspaper3k first
            article = Article(item['url'], config=config)
            article.download()
            article.parse()
            if article.text and len(article.text) > 100:
                articles.append({
                    'ticker': ticker,
                    'title': item['title'],
                    'text': article.text,
                    'source': item['source']['name'],
                    'url': item['url']
                })
                print(f"Success: {item['url']} (newspaper3k)")
                continue

            # Fallback to BeautifulSoup if newspaper3k fails
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://www.google.com/'
            }
            response = requests.get(item['url'], headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract text from common article tags
                paragraphs = soup.find_all('p')
                text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                if text and len(text) > 100:
                    articles.append({
                        'ticker': ticker,
                        'title': item['title'],
                        'text': text,
                        'source': item['source']['name'],
                        'url': item['url']
                    })
                    print(f"Success: {item['url']} (BeautifulSoup)")
                else:
                    print(f"Skipped {item['url']}: Insufficient text")
            else:
                print(f"Skipped {item['url']}: HTTP {response.status_code}")
        except Exception as e:
            print(f"Error processing {item['url']}: {str(e)}")
    
    return pd.DataFrame(articles)

if __name__ == "__main__":
    api_key = "559e2fc66de145a5920ffbdd7e2676f1"  # Replace with your NewsAPI key
    tickers = ["AMZN"]
    news_df = pd.concat([scrape_news_newsapi(ticker, api_key) for ticker in tickers], ignore_index=True)
    news_df.to_csv("raw_news.csv", index=False)
    print(f"Scraped {len(news_df)} articles")