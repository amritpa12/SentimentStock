import requests
import newspaper
from newspaper import Article

params = {
    'q': 'AAPL',
    'tbm': 'nws',
    'api_key': 'a626c79193dd99236a04c2ad028a9f77354583a824628c8f1bbd38c6688f4de5'
}


response = requests.get('https://serpapi.com/search', params=params)
news_results = response.json().get('news_results', [])

#print(news_results)


testArticle = Article('https://finance.yahoo.com/news/trump-does-tim-apple-a-solid-investors-cheer-smartphone-tariff-exemption-despite-mixed-white-house-signals-124235436.html')
testArticle.download()
testArticle.parse()
print(testArticle.text)




article_urls = [article['link'] for article in news_results]

#print(article_urls)
