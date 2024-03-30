import requests
from bs4 import BeautifulSoup
import json

# URL сайту для парсингу цитат
url = "http://quotes.toscrape.com"

# Функція для отримання посилань на всіх авторів зі сторінки
def get_author_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    author_links = [a['href'] for a in soup.select('.author + a')]
    return author_links

# Функція для отримання даних про автора
def get_author_data(author_link):
    author_url = url + author_link
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fullname = soup.select_one('.author-title').get_text(strip=True)
    born_date = soup.select_one('.author-born-date').get_text(strip=True)
    born_location = soup.select_one('.author-born-location').get_text(strip=True)
    description = soup.select_one('.author-description').get_text(strip=True)
    author_data = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }
    return author_data

# Функція для отримання цитат та їх авторів зі сторінки
def get_quotes_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = []
    for quote in soup.select('.quote'):
        text = quote.select_one('.text').get_text(strip=True)
        author = quote.select_one('.author').get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in quote.select('.tag')]
        quote_data = {
            "quote": text,
            "author": author,
            "tags": tags
        }
        quotes.append(quote_data)
    return quotes

# Отримання посилань на всіх авторів
author_links = get_author_links(url)

# Отримання даних про кожного автора
authors_data = [get_author_data(link) for link in author_links]

# Збереження даних про авторів у файл authors.json
with open('authors.json', 'w') as file:
    json.dump(authors_data, file, ensure_ascii=False, indent=4)

# Отримання цитат зі сторінки та збереження даних у файл quotes.json
quotes_data = get_quotes_data(url)
with open('quotes.json', 'w') as file:
    json.dump(quotes_data, file, ensure_ascii=False, indent=4)

print("Дані успішно збережено у файлах authors.json та quotes.json.")
