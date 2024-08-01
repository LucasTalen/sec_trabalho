from django.shortcuts import render, get_object_or_404
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


@csrf_exempt
def perfil_funcionario(request, cpf):
    funcionario = get_object_or_404(Funcionario, CPF=cpf)
    print(funcionario.nascimento)
    return render(request, 'site_sec/perfil.html', {'funcionario':funcionario})


@csrf_exempt
def editar_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('full-name')
        cpf = request.POST.get('cpf')
        nascimento = request.POST.get('dob')
        telefone = request.POST.get('phone')
        cargo = request.POST.get('position')
        email = request.POST.get('email')
        foto_de_perfil = request.FILES.get('profile-pic')
        
        print(cpf)
        print(nome)
        
        funcionario = get_object_or_404(Funcionario, CPF=cpf)
        
                
        funcionario.nome=nome
        
        funcionario.CPF=cpf
        funcionario.nascimento=nascimento
        funcionario.email=email
        funcionario.telefone=telefone
        funcionario.cargo=cargo
        if foto_de_perfil:
            funcionario.foto_perfil=foto_de_perfil
        funcionario.save()
        
        return render(request, f'site_sec/perfil.html')
