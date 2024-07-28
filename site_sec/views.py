from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Funcionario


# Create your views here.
@csrf_exempt
def home(request):
    return render(request, 'site_sec/home.html')

def buscar_funcionario(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        query = request.GET.get('term', '')
        sugestao = Funcionario.objects.filter(nome__icontains=query)[:10]
        resultado = [{'nome':funcionario.nome, 'cpf':funcionario.CPF} for funcionario in sugestao]
        return JsonResponse(resultado, safe=False)
    return JsonResponse({'error':'Request invalida'}, status=400)
