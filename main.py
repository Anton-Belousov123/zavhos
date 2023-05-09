import dataclasses

import requests
from bs4 import BeautifulSoup


@dataclasses.dataclass
class Card:
    name: str
    url: str
    price: float
    photo: str


def scrape_cards(page_source: str):
    soup = BeautifulSoup(page_source, features='html.parser')
    cards_code = soup.find_all('form', {'itemprop': "itemListElement"})
    return cards_code


def scrape_card(card_source: str):
    name = card_source.find('a', {'class': 'card-title'}).text
    url = card_source.find('a', {'class': 'card-title'}).get('href')
    price = float(card_source.find('span', {'class': 'price-span'}).text.split()[0].strip())
    photo = 'https://zavhoz-spb.ru' + card_source.find('img').get('src')
    return Card(
        name=name,
        url=url,
        price=price,
        photo=photo
    )


def scrape_parse_links():
    url = 'https://zavhoz-spb.ru/'
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, features='html.parser')
    elements = soup.find('aside').find_all('a')
    hrefs = []
    for element in elements:
        hrefs.append(element.get('href'))
    return hrefs


def scrape_category(category_link):
    page_number = 0
    print(category_link)
    cards = []
    errors = 0
    while True:
        page_number += 1
        request_url = category_link + f'?page={page_number}'
        response = requests.get(url=request_url)
        if response.url == category_link and page_number != 1:
            break
        cards_codes = scrape_cards(response.text)
        for card_code in cards_codes:
            try:
                card = scrape_card(card_code)
                cards.append(card)
            except:
                errors += 1
    return cards



categories = scrape_parse_links()

for category in categories:
    cards = scrape_category(category)
