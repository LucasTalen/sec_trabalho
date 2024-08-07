from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Funcionario, ExtrasFuncionario
from django.db.models import Max


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
    validade = data_mais_recente_treinamento(cpf)
    lista_atestado, lista_advertencia = dados_extra_funcionario(cpf)
    response = render(request, 'site_sec/perfil.html', {
        'funcionario':funcionario,
        'validade':validade,
        'atestados':lista_atestado,
        'advertencias':lista_advertencia
        })
    response.set_cookie('cpf', cpf)
    return response

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

@csrf_exempt
def editar_extra_funcionario(request):
    if request.method == 'POST':
        cpf = request.session.get('cpf')
        validade = request.POST.get('validade')
        historico_text = request.POST.get('historico_text')
        historico_file = request.FILES.get('historico_file')
        atestado = request.FILES.get('atestado')
        outros = request.POST.get('outros')
        
        funcionario = get_object_or_404(Funcionario, CPF=cpf)
        
        ExtrasFuncionario(
            funcionario=funcionario,
            validade_treinamento=validade,
            advertencia_obs=historico_text,
            advertencia_anexo=historico_file,
            atestado_obs=outros,
            atestado_anexo=atestado            
        ).save()
        return render(request, f'site_sec/home.html')
        
        
def data_mais_recente_treinamento(cpf):
    funcionario = get_object_or_404(Funcionario, CPF=cpf)
    validade = ExtrasFuncionario.objects.filter(funcionario=funcionario).aggregate(Max('validade_treinamento'))
    return validade['validade_treinamento__max']

def dados_extra_funcionario(cpf):
    funcionario = get_object_or_404(Funcionario, CPF=cpf)
    extras = ExtrasFuncionario.objects.filter(funcionario=funcionario)
    atestado_list = []
    advertencia_list = []
    
    for extra in extras:
        if extra.atestado_obs or extra.atestado_anexo:
            atestado_list.append({
                'atestado_obs': extra.atestado_obs,
                'atestado_anexo':extra.atestado_anexo.url if extra.atestado_anexo else None
            })
    
        if extra.advertencia_obs or extra.advertencia_anexo:
            advertencia_list.append({
                'advertencia_obs':extra.advertencia_obs,
                'advertencia_anexo':extra.advertencia_anexo.url if extra.advertencia_anexo else None
            })
 
    return atestado_list, advertencia_list