
from django.forms import ModelForm, widgets
from tarefas.models import ListaTarefas



class ListaTarefasForm(ModelForm):
    class Meta():
        model = ListaTarefas
        fields = ['nome', 'descricao', 'realizada']
        widgets = {
            'realizada': widgets.CheckboxInput(attrs={'class': 'form-check-input'} ),

        }


