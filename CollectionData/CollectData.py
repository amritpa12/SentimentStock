from googlenews import GoogleNews
from newspapert import Article
import pandas as pd


def scrape_news(ticker, max_articles=20):
    gn = GoogleNews(lang='en', period='30d')
    gn.search(f"{ticker} stock")
    articles = []
    credible_sources = ["Reuters", "Bloomberg", "WSJ", "CNBC", "Financial Times", "Wall Street Journal", "New York Times", "The Wall Street Journal", "The New York Times", "The Financial Times"]
    for item in gn.results()[:max_articles]:
        try:
            article = Article(item['link'])
            article.download()
            article.parse()
            if article.text and len(article.text) > 100 and item['media'] in credible_sources:
                articles.append({
                    'title': article.title,
                    'text': article.text,
                    'source': item['media'],
                    'url': item['link']
                })
        except Exception as e:
            print(f"Error processing article {item['link']}: {e}")
    gn.clear()
    return pd.DataFrame(articles)

tickers = ["AAPL", "TSLA", "MSFT"]
news_df = pd.concat([scrape_news(ticker) for ticker in tickers], ignore_index=True)
news_df.to_csv("raw_news.csv", index=False)
print(f"Scraped {len(news_df)} articles")
