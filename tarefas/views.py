from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from tarefas.models import ListaTarefas
from tarefas.forms import ListaTarefasForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
# Create your views here.

@login_required
def home(request):

    lista = ListaTarefas.objects.filter(usuario=request.user)
    return render(request, "tarefas/home.html", {
        "lista": lista,
    })

@login_required
def adicionar(request):

    if request.method == 'POST':
        nome = request.POST['nome']
        descricao = request.POST['descricao']
        concluida = False
        if 'realizada' in request.POST:
            concluida = True
        tarefa = ListaTarefas(nome=nome, usuario=request.user , descricao=descricao, realizada=concluida)
        tarefa.save()
        return redirect("tarefas:home")

    return render(request, "tarefas/adicionar.html", {
        "form": ListaTarefasForm(),
    })   

@login_required
def editar(request, id_item):

    item = ListaTarefas.objects.get(pk=id_item)
    if request.user != item.usuario:
        raise PermissionDenied
    if request.method == 'POST':
        item_editado = request.POST
        item.nome = item_editado['nome']
        item.descricao = item_editado['descricao']
        if 'realizada' in request.POST:
            item.realizada = True
        else:
            item.realizada = False
        item.save()
        return redirect("tarefas:home")
    return render(request, "tarefas/editar.html", {
        "item": item
    })


@login_required
def deletar_tarefa(request, id_item):
    if request.method == 'POST':
        item = ListaTarefas.objects.get(pk=id_item)
        if request.user != item.usuario:
            raise PermissionDenied
        item.delete()
    return redirect("tarefas:home")

