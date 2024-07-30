from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Funcionario


# Create your views here.
@csrf_exempt
def home(request):
    return render(request, 'site_sec/home.html')

@csrf_exempt
def cadastrar_funcionario(request):
    return render(request, 'site_sec/cadastrar_funcionario.html')

@csrf_exempt
def criar_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('full-name')
        cpf = request.POST.get('cpf')
        nascimento = request.POST.get('dob')
        telefone = request.POST.get('phone')
        cargo = request.POST.get('position')
        email = request.POST.get('email')
        foto_de_perfil = request.FILES.get('profile-pic')
                
        Funcionario(
            nome=nome,
            CPF=cpf,
            nascimento=nascimento,
            email=email,
            telefone=telefone,
            cargo=cargo,
            foto_perfil=foto_de_perfil
        ).save()
        
        return render(request, 'site_sec/cadastrar_funcionario.html')

@csrf_exempt
def buscar_funcionario(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        sugestao = Funcionario.objects.filter(nome__icontains=query)[:5]
        if len(sugestao) == 0:
            sugestao = Funcionario.objects.filter(CPF__icontains=query)[:5]
            
        resultado = [{'nome':funcionario.nome, 'cpf':funcionario.CPF} for funcionario in sugestao]
        return JsonResponse(resultado, safe=False)
    return JsonResponse({'error':'Request invalida'}, status=400)
