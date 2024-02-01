import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scrapeo_django.settings")
import django
django.setup()

import requests
from bs4 import BeautifulSoup
from ScrapeoApp.models import News, UserNews
from django.contrib.auth.models import User
from datetime import datetime
import re


def buscar_noticias(category, fecha_inicio, fecha_limite, user_id):
    base_url = f'https://elpais.com/noticias/{category}/'
    page = 0

    # Convertir fechas en un objeto datetime
    fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_limite_dt = datetime.strptime(fecha_limite, '%Y-%m-%d')

    try:
        while True:
            if page == 0:
                url = base_url
            else:
                url = f'https://elpais.com/noticias/{category}/{page}/'

            print('URL de la solicitud:', url)
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                news = soup.find_all('article', class_='c c-d c--m')

                for article in news:
                    # extraer el título de la noticia
                    title_element = article.find('h2', class_='c_t')
                    title = title_element.text.strip() if title_element else "Títle not found"

                    # Encontrar el elemento "a" con id="sc_date"
                    date_element = article.find('a', id='sc_date')

                    # Obtener el valor del atributo data-date
                    full_date = date_element['data-date']

                    # Dividir la cadena de fecha y hora en T
                    date_time = full_date.split('T')

                    # Obtener solo la parte de la fecha (antes de la T)
                    date = date_time[0]

                    # Eliminar la información de la zona horaria
                    date_str = re.sub(r'\+\d{2}:\d{2}', '', full_date)

                    # Verificar si la noticia es anterior al parámetro
                    news_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')

                    # Verificar si la noticia es posterior o igual a la fecha inicio y anterior o igual a la fecha límite
                    if fecha_inicio_dt <= news_date <= fecha_limite_dt:
                        print(f'Se encontró una noticia dentro del rango de fechas con fecha {news_date}. Procesando la noticia.')

                    else:
                        # Verificar si la noticia es anterior a la fecha de inicio
                        if news_date < fecha_inicio_dt:
                            print(f'La noticia "{title}" es anterior a la fecha de inicio {news_date}. Deteniendo la búsqueda.')
                            return
                        else:
                            print(f'La noticia "{title}" no está dentro del rango de fechas {news_date}. Ignorando la noticia.')
                            continue

                    # extraer el enlace de la noticia
                    link_element = title_element.find('a') if title_element else None
                    link = link_element['href'] if link_element else "Enlace no encontrado"

                    # Busca el enlace específico y extrae el texto
                    tag_element = article.find('a', class_='c_k')
                    tag = tag_element.text if tag_element else "Categoría no encontrada"
                    tag = tag.upper()

                    # extraer el autor de la noticia
                    author_element = article.find('a', class_='c_a_a')
                    author = author_element.text.strip() if author_element else "Autor no encontrado"

                    # extraer el contenido de la noticia
                    content_element = article.find('p', class_='c_d')
                    content = content_element.text.strip() if content_element else "Contenido no encontrado"

                    # Verificar si el usuario ya tiene la noticia asociada
                    user_obj = User.objects.get(id=user_id)

                    # Obtener el ID de la noticia si ya existe
                    news_id = News.objects.filter(Title=title).first().pk if News.objects.filter(Title=title).exists() else None

                    # Verificar si una noticia con el mismo título ya existe en la base de datos
                    existing_news = News.objects.filter(Title=title).first()

                    if existing_news:
                        print(f'News "{title}" ya existe en la base de datos.')

                        # Verificar si ya existe una asociación entre el usuario y la noticia
                        if not UserNews.objects.filter(user=user_obj, news=existing_news).exists():
                            # Crear un objeto UserNews y asociarlo con el usuario y la noticia
                            user_news_obj = UserNews(user=user_obj, news=existing_news)
                            user_news_obj.save()
                            print(f'Asociación creada para el usuario y la noticia existente.')
                        else:
                            print(f'La asociación entre el usuario y la noticia ya existe.')
                        continue

                    # imprimir el título, el enlace y el autor
                    print(f'Título: {title}')
                    print(f'Enlace: {link}')
                    print(f'Autor: {author}')
                    print(f'Fecha: {date}')
                    print(f'Contenido: {content}')
                    print(f'Categoría: {tag}')
                    print('-' * 50)

                    # Crear un nuevo objeto Noticia y guardarlo en la base de datos
                    noticia_obj = News(
                        Title=title,
                        Tag=tag,
                        Author=author,
                        Date=date,
                        Link=link,
                        Content=content
                    )
                    noticia_obj.save()

                    # Crear un objeto UserNews y asociarlo con el usuario y la noticia
                    user_news_obj = UserNews(user=user_obj, news=noticia_obj)
                    user_news_obj.save()

                # Incrementar la página para consultar la siguiente
                page += 1
            else:
                raise Exception("Error al consultar la página")


    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

if __name__ == "__main__":
    buscar_noticias(category='expolios', fecha_inicio='2023-12-12', fecha_limite='2024-01-14', user_id=1)
