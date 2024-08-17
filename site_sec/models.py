from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.

profile_image_storage = FileSystemStorage(location='media/profile_images')
profile_advertencia_storage = FileSystemStorage(location='media/profile_advertencia')
profile_atestado_storage = FileSystemStorage(location='media/profile_atestado')

class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    CPF = models.CharField(max_length=14, primary_key=True)
    nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=50)
    admissao = models.DateField()
    matricula = models.CharField(max_length=50)
    foto_perfil = models.ImageField(upload_to='profile_images/',)
    
    def __str__(self):
        return self.nome
    
    
class ExtrasFuncionario(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    validade_treinamento = models.DateField()
    advertencia_obs = models.TextField()
    advertencia_anexo = models.FileField(upload_to='profile_advertencia/%Y/%m/%d/')
    atestado_obs = models.TextField()
    atestado_anexo = models.FileField(upload_to='profile_atestado/%Y/%m/%d/')
    