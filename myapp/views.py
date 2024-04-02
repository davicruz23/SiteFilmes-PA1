from django.shortcuts import render
import requests
from .models import Filme
from django.core.paginator import Paginator


# Create your views here.
def mysite(request):
    
    return render(request, 'index.html')


def browse(request):
    # Lógica da visualização
    return render(request, 'browse.html')

def details(request):
    # Lógica da visualização
    return render(request, 'details.html')

def streams(request):
    # Lógica da visualização
    return render(request, 'streams.html')

def profile(request):
    # Lógica da visualização
    return render(request, 'profile.html')



def video_list(request):
    # URL da API do TMDb para descobrir vídeos
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US"
    # Chave de API do TMDb
    api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"  # Substitua pela sua chave de API do TMDb
    # Cabeçalhos da requisição
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
    }
    # Parâmetros da requisição
    params = {
        "api_key": api_key,
        "sort_by": "popularity.desc"  # Você pode ajustar os parâmetros de acordo com sua necessidade
    }

    # Faça a requisição à API do TMDb
    response = requests.get(url, headers=headers, params=params)

    # Verifique se a resposta foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Se sim, obtenha os vídeos
        videos = response.json()["results"]
        
        # Paginação
        paginator = Paginator(videos, 10)  # Mostra 10 vídeos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Renderize o template 'video_list.html' passando os vídeos como contexto
        return render(request, 'video_list.html', {'page_obj': page_obj})
    else:
        # Se não, exiba uma mensagem de erro
        error_message = f"Erro ao listar vídeos: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})
    


def search_movies(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        # URL da API do TMDb para pesquisar filmes
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=en-US&page=1"
        # Chave de API do TMDb
        api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"  # Substitua pela sua chave de API do TMDb
        # Cabeçalhos da requisição
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
        }
        # Parâmetros da requisição
        params = {
            "api_key": api_key,
            "sort_by": "popularity.desc"  # Você pode ajustar os parâmetros de acordo com sua necessidade
        }
        
        # Faça a requisição à API do TMDb
        response = requests.get(url, headers=headers, params=params)
        
        # Verifique se a resposta foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Se sim, obtenha os filmes
            movies = response.json()["results"]
            # Renderize o template 'search_results.html' passando os filmes como contexto
            return render(request, 'search_results.html', {'movies': movies, 'query': query})
        else:
            # Se não, exiba uma mensagem de erro
            error_message = f"Erro ao pesquisar filmes: {response.status_code}"
            return render(request, 'error.html', {'error_message': error_message})
    
    # Se a solicitação não contiver uma consulta, retorne uma página de pesquisa vazia
    return render(request, 'search_form.html')