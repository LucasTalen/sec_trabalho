from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Funcionario, ExtrasFuncionario
from django.db.models import Max
from django.conf import settings
from .utils.emissor_crachar import *
from datetime import datetime



# Create your views here.
@csrf_exempt
def home(request):
    response = redirect('/')
    for cookie in request.COOKIES:
        response.delete_cookie(cookie)
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
        matricula = request.POST.get('matricula')
        admissao = request.POST.get('admissao')
        foto_de_perfil = request.FILES.get('profile-pic')
                
        Funcionario(
            nome=nome,
            CPF=cpf,
            nascimento=nascimento,
            email=email,
            telefone=telefone,
            cargo=cargo,
            matricula=matricula,
            admissao=admissao,
            foto_perfil=foto_de_perfil
        ).save()
        
        return redirect(f'/perfil/{cpf}/')

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
    # response.set_cookie('cpf', cpf)
    try:
        os.remove("crachas.pdf")
    except:
        ...
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
        matricula = request.POST.get('matricula')
        admissao = request.POST.get('admissao')
        
        foto_de_perfil = request.FILES.get('profile-pic')
        funcionario = get_object_or_404(Funcionario, CPF=cpf)
        
                
        funcionario.nome=nome
        
        funcionario.CPF=cpf
        funcionario.nascimento=nascimento
        funcionario.email=email
        funcionario.telefone=telefone
        funcionario.cargo=cargo
        funcionario.matricula=matricula
        funcionario.admissao=admissao
        if foto_de_perfil:
            funcionario.foto_perfil=foto_de_perfil
        funcionario.save()
        
        return redirect(f'/perfil/{cpf}/')

@csrf_exempt
def editar_extra_funcionario(request):
    if request.method == 'POST':
        
        url = request.META.get('HTTP_REFERER', None)
        url_separada = url.split('/')
        cpf = url_separada[4]
        # print(url_separada)
            
        validade = request.POST.get('validade')
        if not validade:
            validade = datetime.now()
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
        return redirect(f'/perfil/{cpf}/')
    
    
@csrf_exempt
def gerar_crachar(request, cpf):

    funcionario = get_object_or_404(Funcionario, CPF=cpf)
    image_path = os.path.join(settings.MEDIA_ROOT, funcionario.foto_perfil.name)
    
    badges_info = {
        "image_path":  image_path,
        "qrcode":"qr_code.png",
        "name": funcionario.nome,
        "matricula": funcionario.matricula,
        "cargo": funcionario.cargo,
        "cpf": funcionario.CPF
        }
    
    
    output_pdf = "crachas.pdf"
    generate_pdf(badges_info, output_pdf, front_background_path, back_background_path)
    
    
    with open(output_pdf, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_pdf)}"'
        
        return response
        
        
def apagar_funcionario(request, cpf):
    funcionario = get_object_or_404(Funcionario, CPF=cpf)
    funcionario.delete()
    return redirect('/')
    
        
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
                'atestado_anexo':extra.atestado_anexo.url if extra.atestado_anexo else None,
                'id':extra.id
            })
    
        if extra.advertencia_obs or extra.advertencia_anexo:
            advertencia_list.append({
                'advertencia_obs':extra.advertencia_obs,
                'advertencia_anexo':extra.advertencia_anexo.url if extra.advertencia_anexo else None,
                'id': extra.id
            })
 
    return atestado_list, advertencia_list


def apagar_historico(request, cpf, id):
    
    extra = get_object_or_404(ExtrasFuncionario, id=id, funcionario__CPF=cpf)
    
    
    if 'atestado' in request.GET:
        if extra.atestado_anexo:
            extra.atestado_anexo.delete(save=False)  
            extra.atestado_anexo = None  #
        if 'limpar_obs' in request.GET:
            extra.atestado_obs = ''  
    elif 'advertencia' in request.GET:
        if extra.advertencia_anexo:
            extra.advertencia_anexo.delete(save=False)
            extra.advertencia_anexo = None
        if 'limpar_obs' in request.GET:
            extra.advertencia_obs = ''  
    
    extra.save()
   
    return redirect(f'/perfil/{cpf}/')