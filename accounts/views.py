from django.shortcuts import render, redirect
from .admin import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

# Create your views here.
def register(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect('mysite')

        else:
            print('invalid registration details')
            
    return render(request, "registration/register.html",{"form": form})


def logout(request):
    auth_logout(request)
    return redirect('mysite')  # Ou outra página que desejar redirecionar
