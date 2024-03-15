from django.shortcuts import render

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