from movies.models import Movie
from django.shortcuts import render, redirect
from movies.parser import parse_movie_details
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Настройки для Selenium
options = Options()
options.add_argument("--headless")  # Включаем headless режим
options.add_argument("--disable-gpu")  # Отключаем GPU для стабильности
options.add_argument("--no-sandbox")
service = Service('geckodriver')


def load_movies(request):
    if request.method == 'POST':
        movie_urls = get_all_movie_urls()  # Получаем список всех URL фильмов
        movies_data = []  # Список для хранения данных о фильмах

        for movie_url in movie_urls:
            movie_data = parse_movie_details(movie_url)  # Парсим каждую страницу фильма
            movies_data.append(movie_data)

        movies_data.sort(key = lambda x: x['rating_imdb'], reverse = True)

        # Очистка старых данных и запись новых в базу данных
        Movie.objects.all().delete()  # Удаляем старые данные перед загрузкой новых

        for movie in movies_data:
            Movie.objects.create(
                title=movie['title'],
                year=movie['year'],
                director=movie['director'],
                imdb_rating=movie['rating_imdb'],
                description=movie['description'],
                poster=movie['poster'],
            )

        return redirect('movies_view')

def get_all_movie_urls():
    url = 'https://www.film.ru/online'
    driver = webdriver.Firefox(service=service, options=options)
    driver.get(url)
    movie_urls = []

    def scroll(driver, max_movies=100):
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(movie_urls) < max_movies:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(1)
            new_height = driver.execute_script("return document.body.scrollHeight")

            soup = BeautifulSoup(driver.page_source, 'lxml')
            for movie_block in soup.select('div.redesign_afisha_movie'):
                link_to_movie = movie_block.select_one('a.wrapper_block_stack')['href']
                movie_url = f'https://www.film.ru{link_to_movie.replace("/online", "")}'
                if movie_url not in movie_urls:
                    movie_urls.append(movie_url)

                if len(movie_urls) >= max_movies:
                    break

            if new_height == last_height:
                break
            last_height = new_height

    scroll(driver)

    driver.quit()
    return movie_urls

def movies_view(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})
