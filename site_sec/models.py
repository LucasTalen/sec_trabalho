from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

profile_image_storage = FileSystemStorage(location='media/profile_images')

class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    CPF = models.CharField(max_length=11, primary_key=True)
    nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=50)
    foto_perfil = models.ImageField(upload_to='profile_images/',)
    
    def __str__(self):
        return self.nome