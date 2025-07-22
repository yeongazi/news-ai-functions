import requests
from bs4 import BeautifulSoup

def crawl_bbc(limit=10):
    url = "https://www.bbc.com/news/world"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []
    for h3 in soup.select("h3"):
        title = h3.get_text()
        a_tag = h3.find_parent("a")
        if a_tag:
            link = a_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.bbc.com" + link
            articles.append({
                "source": "BBC",
                "title": title,
                "url": link,
                "published": "",
                "content": ""
            })
        if len(articles) >= limit:
            break
    return articles

def crawl_cnn(limit=5):
    url = "https://edition.cnn.com/world"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []
    for span in soup.select("span.container__headline-text"):
        title = span.get_text()
        a_tag = span.find_parent("a")
        link = "https://edition.cnn.com" + a_tag.get("href") if a_tag else None
        articles.append({
            "source": "CNN",
            "title": title,
            "url": link,
            "published": "",
            "content": ""
        })
        if len(articles) >= limit:
            break
    return articles

def crawl_reuters(limit=5):
    url = "https://www.reuters.com/world/"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    articles = []
    for h3 in soup.select("h3"):
        title = h3.get_text(strip=True)
        a_tag = h3.find_parent("a")
        if a_tag:
            link = a_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.reuters.com" + link
            articles.append({
                "source": "Reuters",
                "title": title,
                "url": link,
                "published": "",
                "content": ""
            })
        if len(articles) >= limit:
            break
    return articles
