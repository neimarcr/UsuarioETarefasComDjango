from django.shortcuts import redirect, render
from .forms import UsuarioForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return redirect("tarefas:home")

    return render(request, "usuario/index.html")


def cadastrar_usuario(request):

    if request.user.is_authenticated:
        return redirect("tarefas:home")

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            user = User.objects.create_user(nome, email, senha)
            user.save()
            return redirect("usuario:index")
    
    return render(request, "usuario/cadastrar_usuario.html", {
        "form": UsuarioForm()
    })


def login_user(request):

    if request.user.is_authenticated:
        return redirect("tarefas:home")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            senha = form.cleaned_data['senha']
            user = authenticate(username=nome, password=senha)
            if user:
                login(request, user)
                return redirect("tarefas:home")
            else:
                return render(request, "usuario/login.html", {
                    "form": LoginForm(),
                    "mensagem": "Usuário ou senha está incorreto"
                })

    return render(request, "usuario/login.html", {
        "form": LoginForm()
    })


def logout_user(request):
    logout(request)
    return redirect("usuario:index")


