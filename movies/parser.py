import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import urljoin

url = 'https://www.film.ru/online'


def parse_movie_details(movie_url):
    response = requests.get(movie_url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')

    title_with_year = soup.select_one('h1').get_text(strip = True)
    title = re.sub(r'\s*\(.*?\)\s*', '', title_with_year)
    year = soup.select_one('h1 span').get_text(strip = True)

    rating = soup.select('.wrapper_movies_scores_score')

    # Извлечение только числового значения из рейтинга
    if len(rating) > 1:
        rating_text = rating[1].get_text(strip = True)
        # Используем регулярное выражение для извлечения числового значения
        rating_imdb = re.search(r'\d+\.\d+', rating_text)
        rating_imdb = float(rating_imdb.group(0)) if rating_imdb else 0.0
    else:
        rating_imdb = 0.0  # Значение по умолчанию, если рейтинг отсутствует

    director = soup.select_one('.block_table:-soup-contains("режиссер") + div a').get_text(strip = True) if soup.select_one(
        '.block_table:-soup-contains("режиссер") + div a') else 'Нет данных'
    description = soup.select_one('.wrapper_movies_text').get_text(strip = True)

    poster_tag = soup.select_one('.wrapper_block_stack.wrapper_movies_poster')
    poster_url = urljoin(movie_url, poster_tag['data-src']) if poster_tag and 'data-src' in poster_tag.attrs else None

    poster_path = None
    if poster_url:
        poster_response = requests.get(poster_url)
        poster_response.raise_for_status()

        os.makedirs('media/movies/posters', exist_ok = True)

        poster_name = f"{title.replace(' ', '_').replace('/', '-')}.jpg"  # Форматирование имени файла
        poster_path = os.path.join('media/movies/posters', poster_name)  # Изменено на 'posters'

        with open(poster_path, 'wb') as f:
            f.write(poster_response.content)

    return {
        'title': title,
        'year': year,
        'rating_imdb': rating_imdb,
        'director': director,
        'description': description,
        'poster': poster_path,
    }


response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')

#  search info block
movies = []
for movie_block in soup.select('div.redesign_afisha_movie'):
    link_to_movie = movie_block.select_one('a.wrapper_block_stack')['href']
    movie_url = f'https://www.film.ru{link_to_movie.replace("/online", "")}'

    movie_details = parse_movie_details(movie_url)
    movies.append(movie_details)