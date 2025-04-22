from polygon import RESTClient
import csv
import os
from dotenv import load_dotenv, dotenv_values
import openai

load_dotenv()

# Initialize Polygon client
client = RESTClient(os.getenv("polygonKey"))
openai.api_key = ""


def sentimentToCSV(ticker_symbol, publish_date):
    news_articles = client.list_ticker_news(
        ticker_symbol,
        params={"published_utc.gte": publish_date},
        order="desc",
        limit=1000
    )
    csv_file = f"{ticker_symbol}_news_sentiment.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Sentiment", "Sentiment Reasoning", "URL"])
        for article in news_articles:
            writer.writerow([
                article.title,
                article.insights[0].sentiment,
                article.insights[0].sentiment_reasoning,
                article.article_url
            ])
    returnStatement = f"Data successfully exported to {csv_file}" 
    return returnStatement











ticker = "AAPL"
datePublish = "2025-04-10" # Year - Month - Day 

print(sentimentToCSV(ticker, datePublish))
