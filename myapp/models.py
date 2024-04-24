from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Filme(models.Model):
    api_id = models.IntegerField(unique=False, default=0)

def get_poster_url(self):
        base_url = "https://image.tmdb.org/t/p/w500/"
        return f"{base_url}{self.api_id}"  # Supondo que o ID retornado pela API do TMDB seja o mesmo usado para recuperar o poster



class MyProfile(models.Model):
    user = models.OneToOneField(User, 
                        on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=100)
    dataDeNascimento = models.DateField(default='1900-01-01') 
    fotoPerfil = models.ImageField(upload_to='perfil_fotos/', default='default_profile_pic.jpg')
    filmes = models.ManyToManyField(Filme)
    amigos = models.ManyToManyField('self')
    

@receiver(post_save, sender=User)
def my_handler(sender, **kwargs):
    """
    Quando Criar um usuário no Django, vai rodar essa função
    para criar uma instancia nesse modelo MyProfile no campo "user".
    """
    if kwargs.get('created', False):
        MyProfile.objects.create(user=kwargs['instance'])

class AvaliacaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    voto = models.IntegerField()
    comentario = models.TextField()
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

class Comentario(models.Model):
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
