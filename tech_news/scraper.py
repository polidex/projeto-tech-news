import time
import requests
from parsel import Selector


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


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_news(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
