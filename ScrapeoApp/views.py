import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from django.views import View
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from ScrapeoApp.models import News, Tag

from ScrapeoApp.serializers import NewsSerializer, TagSerializer

from django.http import JsonResponse
from elpais_scrapeo import buscar_noticias
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ejecutar_scraping(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        categoria = data.get('categoria', '')
        fechaLimite = data.get('fechaLimite', '2010-01-01')

        try:
            buscar_noticias(categoria, fechaLimite)
            return JsonResponse({"message": "Script ejecutado correctamente"}, status=200)

        except Exception as e:
            return JsonResponse({"message": f"Ocurrió un error: {str(e)}"}, status=500)

    return JsonResponse({"message": "Método no permitido"}, status=405)


class NewsPagination(PageNumberPagination):
    page_size = 10  # Número de noticias por página

class NoticiaList(generics.ListCreateAPIView):
    queryset = News.objects.order_by('-Date')
    serializer_class = NewsSerializer
    pagination_class = NewsPagination

class NoticiaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BuscarNoticias(generics.ListAPIView):
    serializer_class = NewsSerializer
    pagination_class = NewsPagination

    def get_queryset(self):
        categoria = self.request.query_params.get('categoria', None)
        fechaDesde = self.request.query_params.get('fechaDesde', None)
        fechaHasta = self.request.query_params.get('fechaHasta', None)
        autor = self.request.query_params.get('autor', None)
        palabras_clave = self.request.query_params.get('palabras_clave', None)

        queryset = News.objects.order_by('-Date')

        # Aplicar filtros en base a los parámetros recibidos
        if categoria:
            queryset = queryset.filter(Tag=categoria)
        if fechaDesde:
            fechaDesde = datetime.strptime(fechaDesde, '%Y-%m-%d')
            queryset = queryset.filter(Date__gte=fechaDesde)
        if fechaHasta:
            fecha_hasta = datetime.strptime(fechaHasta, '%Y-%m-%d')
            queryset = queryset.filter(Date__lte=fechaHasta)
        if autor:
            queryset = queryset.filter(Author=autor)
        if palabras_clave:
            print(palabras_clave)
            # Dividir las palabras clave en una lista
            palabras_clave_lista = palabras_clave.split(',')
            # Inicializar una lista de condiciones Q
            condiciones_q = [Q(Title__icontains=palabra) | Q(Content__icontains=palabra) for palabra in palabras_clave_lista]
            # Aplicar todas las condiciones Q con operador OR
            q_objects = Q()
            for condicion in condiciones_q:
                q_objects &= condicion
            # Aplicar las condiciones Q a la consulta
            queryset = queryset.filter(q_objects)

        return queryset

class Autores(View):
    def get(self, request):
        autores = News.objects.values('Author').distinct().order_by('Author')
        autores_list = list(autores.values_list('Author', flat=True))
        return JsonResponse(autores_list, safe=False)

