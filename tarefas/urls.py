from django.urls import path
from tarefas import views

app_name="tarefas"

urlpatterns = [
    path("", views.home, name="home"),
    path("adicionar", views.adicionar, name="adicionar"),
    path("<int:id_item>/editar", views.editar, name="editar"),
    path("<int:id_item>/deletar_tarefa", views.deletar_tarefa, name="deletar_tarefa"),
]