from django.shortcuts import render
from django.core import serializers # NOVA IMPORTAÇÃO
from .models import Produto, Categoria 
# Certifique-se de que outras views também importam o necessário, 
# mas mantive o essencial para o chatbot

def home(request):
    return render(request, 'core/home.html')

def sobre(request):
    return render(request, 'core/sobre.html')

# A view 'chatbot' agora serializa os dados para JSON
def chatbot(request):
    categorias = Categoria.objects.all()
    produtos = Produto.objects.all()

    # Serializa os QuerySets de Django para strings JSON
    categorias_json = serializers.serialize('json', categorias)
    produtos_json = serializers.serialize('json', produtos)

    # Passa as strings JSON serializadas para o template
    return render(request, 'core/chatbot.html', {
        'categorias_json': categorias_json,
        'produtos_json': produtos_json
    })