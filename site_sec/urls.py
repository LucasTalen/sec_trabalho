from django.urls import path
from . import views 


urlpatterns = [
    path('', views.home),
    path('pesquisar/funcionario/', views.buscar_funcionario, name='pesquisar_funcionario')
]

