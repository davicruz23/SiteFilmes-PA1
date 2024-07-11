from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Genero(models.Model):
    nome = models.CharField(max_length=255)

class Filme(models.Model):
    api_id = models.IntegerField(unique=False, default=0)
    generos = models.ManyToManyField(Genero)

    def get_poster_url(self):
        base_url = "https://image.tmdb.org/t/p/w500/"
        return f"{base_url}{self.api_id}"  # Supondo que o ID retornado pela API do TMDB seja o mesmo usado para recuperar o poster

class MyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.CharField(max_length=100)
    dataDeNascimento = models.DateField(default='1900-01-01') 
    fotoPerfil = models.ImageField(upload_to='perfil_fotos/', default='default_profile_pic.jpg')
    filmes = models.ManyToManyField(Filme)
    amigos = models.ManyToManyField('self')
    seguindo = models.ManyToManyField('self', symmetrical=False, related_name='seguidores')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Quando criar um usuário no Django, esta função será executada
    para criar uma instância no modelo MyProfile no campo "user".
    """
    if created:
        MyProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Salva automaticamente o perfil do usuário associado sempre que o modelo User é salvo.
    """
    instance.profile.save()

class AvaliacaoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    voto = models.IntegerField()
    comentario = models.TextField()
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

class Comentario(models.Model):
    comentario = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

class UsuarioGeneroVisto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
