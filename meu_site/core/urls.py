from django.urls import path
from . import views

urlpatterns = [
    # Esta linha agora define o endereço raiz (path='') para chamar a view 'chatbot'
    path('', views.chatbot, name='chatbot'), 
]