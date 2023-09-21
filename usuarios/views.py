from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
from django.contrib import auth 
import re
from zxcvbn import zxcvbn


def cadastro(request):
    if request.method=="GET":
        return render(request,'cadastro.html')
    
    elif request.method=="POST":
       username =request.POST.get('username')
       email=request.POST.get('email')
       senha=request.POST.get('senha')
       confirmar_senha=request.POST.get('confirmar_senha')
       
        # Verifica se as senhas coincidem
       if not senha==confirmar_senha:
           
           messages.add_message(request,constants.ERROR, 'As senha nao coincidem.')
           return redirect(reverse('cadastro'))
        
    # Verifica a força da senha
    if len(senha) < 8:
            messages.add_message(request, constants.ERROR, 'A senha deve ter pelo menos 8 caracteres.')
            return redirect(reverse('cadastro'))
        
        
    elif not re.search('[a-záàâãéèêíïóôõöúüç]', senha):
            messages.add_message(request, constants.ERROR, 'Senha deve conter pelo menos uma letra minúscula.')
            return redirect(reverse('cadastro'))
        
    elif not re.search('[A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇ]', senha):
            messages.add_message(request, constants.ERROR, 'Senha deve conter pelo menos uma letra maiúscula.')
            return redirect(reverse('cadastro'))
        
    elif not re.search('[^a-zA-Z0-9áàâãéèêíïóôõöúüçÁÀÂÃÉÈÊÍÏÓÔÕÖÚÜÇ]', senha):
            messages.add_message(request, constants.ERROR, 'Senha deve conter pelo menos um caractere especial.')
            return redirect(reverse('cadastro'))
     #para avaliar se senha e fraca ou nao    
    
        
    # Verifica se o usuário já existe
    user= User.objects.filter(username=username)
    if user.exists():
        messages.add_message(request,constants.ERROR, 'O usuario ja existes.')
        return redirect(reverse('cadastro'))
    
    # Cria o usuário
    user=User.objects.create_user(username=username,email=email,password=senha)
    messages.add_message(request,constants.SUCCESS, 'Usuario salvo com sucesso.')
    return  redirect(reverse('login'))




def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    
    
    elif request.method=="POST":
       username =request.POST.get('username')
       senha=request.POST.get('senha')
       
       user=auth.authenticate(username=username, password=senha)
       
       if not user:
           messages.add_message(request, constants.ERROR, 'Username ou senha invalida')
           return redirect(reverse('login'))
       
       auth.login(request,user)
       return redirect(reverse('novo_evento'))
    
     