import time
import requests
from parsel import Selector
import re
from tech_news.database import create_news


def fetch(url):
    time.sleep(1)
    try:
        response = requests.get(url, {"user-agent": "Fake user-agent"},
                                timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        return None


def scrape_updates(html_content):
    selector = Selector(text=html_content)

    urls = selector.css('.cs-overlay-link::attr(href)').getall()
    return urls


def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)

    next_page_link = selector.css('.next::attr(href)').get()
    if next_page_link:
        return next_page_link
    else:
        return None


def scrape_news(html_content):
    selector = Selector(text=html_content)

    url = selector.css('link[rel=canonical]::attr(href)').get()
    title = selector.css('.entry-title::text').get()
    timestamp = selector.css('.meta-date::text').get()
    writer = selector.css('.author a::text').get()
    reading_time = selector.css('.meta-reading-time::text').get()
    summary = selector.css('.entry-content p').get()
    category = selector.css('.label::text').get()

    return {
        'url': url,
        'title': title.strip('\xa0'),
        'timestamp': timestamp,
        'writer': writer,
        'reading_time': int(reading_time.split(' ')[0]),
        'summary': re.sub('<.*?>', '', summary).strip(),
        'category': category,
        }


def get_tech_news(amount):
    page = 'https://blog.betrybe.com/'
    scraped_news = []

    while len(scraped_news) < amount:
        response = fetch(page)
        update = scrape_updates(response)
        scraped_news.extend(update)
        page = scrape_next_page_link(response)

    scraped_news_list = []
    for i in scraped_news[:amount]:
        news = scrape_news(fetch(i))
        scraped_news_list.append(news)
    create_news(scraped_news_list)

    return scraped_news_list[:amount]
