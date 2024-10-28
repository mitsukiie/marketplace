from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)
    cep = models.CharField(max_length=8, blank=True)
    endereco = models.CharField(max_length=100, blank=True)
    foto_perfil = models.ImageField(upload_to='icon-profile/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Product(models.Model):
    CONDITION_CHOICES = [
        ('Novo', 'Novo'),
        ('Usado', 'Usado'),
        ('Semi-novo', 'Semi-novo'),
        ('Recondicionado', 'Recondicionado'),
        ('Danificado', 'Danificado'),
    ]

    CATEGORY_CHOICES = [
        ('Roupas', 'Roupas'),
        ('Moveis', 'Móveis'),
        ('Eletrodomesticos', 'Eletrodomésticos'),
        ('Brinquedos', 'Brinquedos'),
        ('Livros', 'Livros'),
        ('Informatica', 'Informática'),
        ('Esportes', 'Esportes'),
        ('Ferramentas', 'Ferramentas'),
        ('Cosmeticos', 'Cosméticos'),
    ]


    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    images = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name