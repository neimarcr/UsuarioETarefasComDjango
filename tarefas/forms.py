
from django.forms import ModelForm, widgets
from tarefas.models import ListaTarefas



class ListaTarefasForm(ModelForm):
    class Meta():
        model = ListaTarefas
        fields = ['nome', 'descricao', 'realizada']
        widgets = {
            'realizada': widgets.CheckboxInput(attrs={'class': 'form-check-input'} ),
            'nome': widgets.TextInput(attrs={'class': 'form-control'}),
            'descricao': widgets.Textarea(attrs={'class': 'form-control'})
        }


# class DeletarTarefa(DeleteView):
#     model = ListaTarefas
#     success_url = reverse_lazy("tarefas:home")