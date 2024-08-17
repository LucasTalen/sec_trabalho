from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views 


urlpatterns = [
    path('', views.home),
    path('pesquisar/funcionario/', views.buscar_funcionario, name='pesquisar_funcionario'),
    path('cadastrar/funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('criar/funcionario/', views.criar_funcionario, name='criar_funcionario'),
    path('editar/funcionario/', views.editar_funcionario, name='editar_funcionario'),
    path('perfil/<str:cpf>/', views.perfil_funcionario, name='perfil_funcionario'),
    path('crachar/<str:cpf>/', views.gerar_crachar, name='crachar_funcionario'),
    path('deletar/<str:cpf>/', views.apagar_funcionario, name='apagar_funcionario'),
    path('funcionario/<str:cpf>/historico/<int:id>/apagar/', views.apagar_historico, name='apagar_historico'),
    path('salvar/detalhes/funcionario/', views.editar_extra_funcionario, name='salvar_detalhes_funcionario'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

