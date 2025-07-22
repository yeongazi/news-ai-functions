import os
import requests

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_news_api(country="us", page_size=30):
    params = {
        "country": country,
        "apiKey": API_KEY,
        "pageSize": page_size
    }
    res = requests.get(BASE_URL, params=params)
    data = res.json()
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "source": a.get("source", {}).get("name", "NewsAPI"),
            "title": a.get("title"),
            "url": a.get("url"),
            "published": a.get("publishedAt"),
            "content": a.get("description", "")
        })
    return articles

