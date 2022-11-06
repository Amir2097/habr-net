import time
import bs4
import requests


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

base_url = 'https://habr.com'
url = base_url + '/ru/all/'

KEYWORDS = ['дизайн', 'фото', 'web', 'python']



response = requests.get(url, headers=headers)
text = response.text
soup = bs4.BeautifulSoup(text, features='html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')

def get_search_key():
    '''Выборка статей, в которых содержится ключевое слово(KEYWORDS)'''
    for article in articles:
        post_url = article.find('a', class_='tm-article-snippet__title-link')
        href = post_url['href']
        post_href = f'{base_url}{href}'
        post = requests.get(post_href, headers=headers)
        soup_post = bs4.BeautifulSoup(post.text, features='html.parser')
        article_post = soup_post.find_all('article', class_= 'tm-article-presenter__content tm-article-presenter__content_narrow')
        time.sleep(1)

        for post_art in article_post:
            previews_type_1 = post_art.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-1")
            previews_type_2 = post_art.find_all(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
            previews_list = [hub.text.strip() for hub in previews_type_2]
            if previews_list == []:
                previews_list = [hub.text.strip() for hub in previews_type_1]

            for previews_text in previews_list:
                for key in KEYWORDS:
                    if key in previews_text:
                        title = article.find('a', class_='tm-article-snippet__title-link')
                        title_name = title.text
                        date_hub = article.find(class_='tm-article-snippet__datetime-published')
                        date_prev = date_hub.time['title']
                        href = article.find('a', class_='tm-article-snippet__title-link')
                        href = href['href']
                        full_href = f'{base_url}{href}'
                        print(f'{date_prev}\n{title_name}\n{full_href}')


if __name__ == '__main__':
    get_search_key()

