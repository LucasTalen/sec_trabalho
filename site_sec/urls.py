from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views 


urlpatterns = [
    path('', views.home),
    path('pesquisar/funcionario/', views.buscar_funcionario, name='pesquisar_funcionario'),
    path('cadastrar/funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('criar/funcionario/', views.criar_funcionario, name='criar_funcionario'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

