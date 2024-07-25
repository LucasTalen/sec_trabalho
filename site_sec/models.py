from django.db import models

# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length=50)
    CPF = models.CharField(max_length=11, primary_key=True)
    nascimento = models.DateField()
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    cargo = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome