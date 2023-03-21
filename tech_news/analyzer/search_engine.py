from tech_news.database import search_news
from datetime import datetime


def search_by_title(title):
    news_list = []
    read_title = search_news({'title': {'$regex': title, '$options': 'i'}})

    for i in read_title:
        news_list.append((i['title'], i['url']))
    return news_list


def search_by_date(date):
    try:
        news_list = []
        read_date = search_news(
            {'timestamp': datetime.fromisoformat(date).strftime('%d/%m/%Y')}
            )

        for i in read_date:
            news_list.append((i['title'], i['url']))
        return news_list
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 9
def search_by_category(category):
    news_list = []
    read_category = search_news(
        {'category': {'$regex': category, '$options': 'i'}}
        )

    for i in read_category:
        news_list.append((i['title'], i['url']))
    return news_list
