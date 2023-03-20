import time
import requests
from parsel import Selector
import re


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


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
