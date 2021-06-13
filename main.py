import requests
from bs4 import BeautifulSoup
import csv


def get_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}
    response = requests.get(url)

    return response


def get_page_content(response):
    soup = BeautifulSoup(response.content, 'lxml')
    page_content = soup.find(id='zg-ordered-list')
    rank_tag = page_content.find_all(class_="zg-badge-text")
    rank = [r.text.strip() for r in rank_tag]
    #book_titles_tag = page_content.find_all(class_="a-link-normal")
    #book_title = [b.text.strip() for b in book_titles_tag]
    book_titles_tag = page_content.find_all(class_="p13n-sc-truncate p13n-sc-line-clamp-1")
    book_pubilshers = page_content.find_all(class_="a-row a-size-small")
    reviews = page_content.find_all(class_="a-size-small a-link-normal")
    price = page_content.find_all(class_="a-link-normal a-text-normal")

    data = []
    for rank, book_title, book_publilsher, review, price in zip(rank_tag, book_titles_tag, book_pubilshers, reviews, price):
        data.append([rank.text, book_title.text.strip(), book_publilsher.text, review.text, float(price.text[1:])])

    return data


def export_data(data):

    with open(f'file.csv', 'w', encoding="utf-8") as output_file:
        headers = ['Rank', 'Book Name', 'Author/Publisher', 'Reviews', 'Price']
        writer = csv.writer(output_file)
        writer.writerow(headers)
        writer.writerows(data)

    print('Data is exported to CSV file')


if __name__ == '__main__':
    url = 'https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_1ie=UTF8&pg=1'
    response = get_data(url)
    content = get_page_content(response)
    export_data(content)

