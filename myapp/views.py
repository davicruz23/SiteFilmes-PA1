from django.shortcuts import render, get_object_or_404, redirect
import requests
from .models import Filme, MyProfile
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import MyProfileForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Filme, Comentario, Genero, UsuarioGeneroVisto
from collections import Counter

def mysite(request):
    
    return render(request, 'index.html')

def browse(request):
    # Lógica da visualização
    return render(request, 'browse.html')

def filme_details(request, filme_id):
    # URL da API do TMDb para obter detalhes do filme
    url = f"https://api.themoviedb.org/3/movie/{filme_id}?language=pt-BR"
    # Chave de API do TMDb
    api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"  # Substitua pela sua chave de API do TMDb
    # Cabeçalhos da requisição
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
    }

    # Parâmetros da requisição
    params = {
        "api_key": api_key
    }

    # Faça a requisição à API do TMDb para obter os detalhes do filme
    response = requests.get(url, headers=headers, params=params)

    # Verifique se a resposta foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Se sim, obtenha os detalhes do filme
        filme = response.json()
        # Renderize o template 'video_details.html' passando os detalhes do filme como contexto
        return render(request, 'details.html', {'filme': filme})
    else:
        # Se não, exiba uma mensagem de erro
        error_message = f"Erro ao obter detalhes do filme: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})

def streams(request):
    # Lógica da visualização
    return render(request, 'streams.html')

@login_required
def profile(request):
    profile = get_object_or_404(MyProfile, user=request.user)
    filmes_vistos = []

    for filme_id in profile.filmes.values_list('api_id', flat=True):  # Obter apenas os IDs dos filmes vistos pelo usuário
        # Fazer uma solicitação para obter os detalhes do filme
        url = f"https://api.themoviedb.org/3/movie/{filme_id}"
        api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"
        params = {
            "api_key": api_key,
            "language": "pt-BR"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            filme_detalhes = response.json()
            titulo_filme = filme_detalhes.get('original_title')
            poster_path = filme_detalhes.get('poster_path')
            if titulo_filme and poster_path:
                filmes_vistos.append({'titulo': titulo_filme, 'poster_url': f"https://image.tmdb.org/t/p/w500/{poster_path}"})

    return render(request, 'profile.html', {'profile': profile, 'filmes_vistos': filmes_vistos})

def update_profile(request):
    profile = request.user.profile  # Obtém o profile do usuário atual
    if request.method == 'POST':
        form = MyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redireciona para a página do profile após a atualização
    else:
        form = MyProfileForm(instance=profile)
    return render(request, 'profile_edit.html', {'form': form, 'profile': profile})

def video_list(request):
    # Obtém todos os gêneros dos filmes vistos pelo usuário
    generos_vistos = UsuarioGeneroVisto.objects.filter(usuario=request.user)
    
    # Conta qual gênero foi visto com mais frequência usando o nome
    genero_contagem = Counter([genero.genero.nome for genero in generos_vistos])
    genero_mais_frequente_nome = genero_contagem.most_common(1)[0][0] if genero_contagem else None
    print(genero_mais_frequente_nome)

    # Obtém o objeto Genero correspondente ao nome mais frequente
    genero_mais_frequente = Genero.objects.get(nome=genero_mais_frequente_nome) if genero_mais_frequente_nome else None

    # Se houver um gênero mais frequente, buscar filmes desse gênero
    if genero_mais_frequente:
        url = f"https://api.themoviedb.org/3/discover/movie?with_genres={genero_mais_frequente.nome}&language=pt-BR"
    else:
        url = "https://api.themoviedb.org/3/movie/popular?language=pt-BR"

    api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
    }
    params = {
        "api_key": api_key,
        "sort_by": "popularity.desc"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        videos = response.json()["results"]
        paginator = Paginator(videos, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Renderiza o template 'video_list.html' passando os vídeos e o gênero mais frequente como contexto
        return render(request, 'video_list.html', {'page_obj': page_obj, 'genero_mais_frequente': genero_mais_frequente})
    else:
        error_message = f"Erro ao listar vídeos: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})

def search_movies(request):
    if 'query' in request.GET:
        query = request.GET.get('query')
        # URL da API do TMDb para pesquisar filmes
        url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=pt-BR&page=1"
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

@login_required
def marcar_visto(request, filme_id):
    if request.method == 'POST':
        # Obter o comentário do formulário
        comentario = request.POST.get('comentario')

        # URL da API do TMDb para obter detalhes do filme
        url = f"https://api.themoviedb.org/3/movie/{filme_id}?language=pt-BR"
        # Chave de API do TMDb
        api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"  # Substitua pela sua chave de API do TMDb
        # Cabeçalhos da requisição
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
        }

        # Parâmetros da requisição
        params = {
            "api_key": api_key
        }

        # Faça a requisição à API do TMDb para obter os detalhes do filme
        response = requests.get(url, headers=headers, params=params)

        # Verifique se a resposta foi bem-sucedida (código 200)
        if response.status_code == 200:
            # Se sim, obtenha os detalhes do filme
            filme = response.json()
            # Salve o ID do filme no modelo Filme
            novo_filme = Filme(api_id=filme_id)
            novo_filme.save()
            
            # Obter e salvar os gêneros do filme
            for genero in filme['genres']:
                genero_obj, created = Genero.objects.get_or_create(nome=genero['id'])
                print(genero_obj)
                novo_filme.generos.add(genero_obj)
                # Salvar a associação entre o usuário e o gênero do filme
                UsuarioGeneroVisto.objects.create(usuario=request.user, genero=genero_obj, filme=novo_filme)
            
            # Salvar o comentário no banco de dados
            Comentario.objects.create(comentario=comentario, usuario=request.user, filme=novo_filme)
            
            # Agora, vincule este filme ao usuário atual
            request.user.profile.filmes.add(novo_filme)
            
            # Renderize o template 'video_details.html' passando os detalhes do filme como contexto
            return render(request, 'details.html', {'filme': filme})
        else:
            # Se não, exiba uma mensagem de erro
            error_message = f"Erro ao obter detalhes do filme: {response.status_code}"
            return render(request, 'error.html', {'error_message': error_message})
    else:
        return redirect('index')  # Redirecionar se o método não for POST

    
def home(request):
    filmes = []  # Inicialize a lista de filmes vazia

    # Verifique se o usuário está autenticado
    if request.user.is_authenticated:
        usuarios = User.objects.exclude(pk=request.user.pk)
        lista_usuarios = []

        for usuario in usuarios:
            perfil = usuario.profile
            sendo_seguido = perfil.seguindo.filter(user=request.user).exists()
            filmes_favoritos = perfil.filmes.all()
            ultimo_api_id = None
            ultimo_comentario = None

            if filmes_favoritos:
                ultimo_filme = filmes_favoritos.last()
                ultimo_api_id = ultimo_filme.api_id if ultimo_filme else None
                
                # Obtenha o último comentário do usuário no último filme visto
                ultimo_comentario = Comentario.objects.filter(usuario=usuario, filme=ultimo_filme).last()

            info_usuario = {
                'usuario': usuario,
                'foto_perfil': perfil.fotoPerfil.url,
                'sendo_seguido': sendo_seguido,
                'ultimo_api_id': ultimo_api_id,
                'imagem_ultimo_filme': None,
                'ultimo_comentario': ultimo_comentario,
            }

            if ultimo_api_id:
                url_filme = f"https://api.themoviedb.org/3/movie/{ultimo_api_id}?language=pt-BR&api_key=bfe8cc9c3791fe2745d71c6b203ad7ab"
                response_filme = requests.get(url_filme)
                if response_filme.status_code == 200:
                    detalhes_filme = response_filme.json()
                    poster_path = detalhes_filme.get('poster_path')
                    if poster_path:
                        info_usuario['imagem_ultimo_filme'] = f"https://image.tmdb.org/t/p/w500{poster_path}"

            lista_usuarios.append(info_usuario)

    # Obtenha os filmes populares, independentemente do status de autenticação
    url = "https://api.themoviedb.org/3/movie/popular?language=pt-BR"
    api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiZmU4Y2M5YzM3OTFmZTI3NDVkNzFjNmIyMDNhZDdhYiIsInN1YiI6IjYzNTJjMTNjYTBmMWEyMDA3OTYzMmZjNyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.AXoon4kjsBMzYtTKRCUTDYR_Jfds9TPYi8okNTHjv5g"
    }
    params = {
        "api_key": api_key,
        "sort_by": "popularity.desc"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        filmes = response.json()["results"]

    context = {
        'lista_usuarios': lista_usuarios if request.user.is_authenticated else None,
        'filmes': filmes
    }

    return render(request, 'index.html', context)




def exibir_perfil_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil = usuario.profile
    filmes_vistos = []

    for filme_id in perfil.filmes.values_list('api_id', flat=True):
        url = f"https://api.themoviedb.org/3/movie/{filme_id}"
        api_key = "bfe8cc9c3791fe2745d71c6b203ad7ab"
        params = {
            "api_key": api_key,
            "language": "pt-BR"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            filme_detalhes = response.json()
            titulo_filme = filme_detalhes.get('original_title')
            poster_path = filme_detalhes.get('poster_path')
            if titulo_filme and poster_path:
                filmes_vistos.append({'titulo': titulo_filme, 'poster_url': f"https://image.tmdb.org/t/p/w500/{poster_path}"})

    # Verificar se o usuário logado está seguindo o usuário do perfil
    sendo_seguido = False
    if request.user.is_authenticated:
        sendo_seguido = perfil.seguidores.filter(user=request.user).exists()

    return render(request, 'perfiluser.html', {'usuario': usuario, 'perfil': perfil, 'filmes_vistos': filmes_vistos, 'sendo_seguido': sendo_seguido})

@login_required
def seguir_usuario(request, username):
    # Obtém o usuário que está sendo seguido
    usuario_seguido = get_object_or_404(User, username=username)
    
    # Verifica se o usuário atual já está seguindo o usuário sendo seguido
    if request.user.profile.seguindo.filter(user=usuario_seguido).exists():
        # Se sim, remove o usuário sendo seguido da lista de seguindo
        request.user.profile.seguindo.remove(usuario_seguido.profile)
    else:
        # Se não, adiciona o usuário sendo seguido à lista de seguindo
        request.user.profile.seguindo.add(usuario_seguido.profile)
    
    # Redireciona de volta para a página atual
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def seguindo(request):
    # Obter a lista de usuários que o usuário logado está seguindo
    usuarios_seguindo = request.user.profile.seguindo.all()
    print(usuarios_seguindo)  # Adicione esta linha para verificar se a lista está sendo populada corretamente
    
    # Renderizar o template 'seguindo.html' passando a lista de usuários como contexto
    return render(request, 'seguindo.html', {'usuarios_seguindo': usuarios_seguindo})


def deixar_seguir(request, username):
    # Obtém o usuário que está sendo seguido
    usuario_seguido = get_object_or_404(User, username=username)
    
    # Verifica se o usuário logado está seguindo o usuário sendo seguido
    if request.user.profile.seguindo.filter(user=usuario_seguido).exists():
        # Se sim, remove o usuário sendo seguido da lista de seguindo
        request.user.profile.seguindo.remove(usuario_seguido.profile)
    
    # Redireciona para a página 'seguindo.html'
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))