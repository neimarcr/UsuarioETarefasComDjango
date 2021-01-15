
from django.forms import ModelForm, widgets
from tarefas.models import ListaTarefas



class ListaTarefasForm(ModelForm):
    class Meta():
        model = ListaTarefas
        fields = ['nome', 'descricao', 'realizada']
        widgets = {
            'realizada': widgets.CheckboxInput
        }

# class DeletarTarefa(DeleteView):
#     model = ListaTarefas
#     success_url = reverse_lazy("tarefas:home")