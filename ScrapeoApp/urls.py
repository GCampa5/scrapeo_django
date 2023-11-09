from django.urls import re_path

from . import views
from .views import Autores

urlpatterns = [
    re_path(r'^noticia$', views.NoticiaList.as_view()),
    re_path(r'^noticia/(?P<pk>[0-9]+)$', views.NoticiaDetail.as_view()),
    re_path('scraping_elpais/', views.ejecutar_scraping, name='ejecutar_scraping'),
    re_path(r'^tag$', views.TagList.as_view()),
    re_path(r'^tag/(?P<pk>[0-9]+)$', views.TagDetail.as_view()),
    re_path('buscar_noticias/', views.BuscarNoticias.as_view(), name='buscar_noticias'),
    re_path('autores/', Autores.as_view(), name='autores')

]