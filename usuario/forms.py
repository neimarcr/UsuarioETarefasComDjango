from django import forms

class UsuarioForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=64, error_messages={ 
                 'required':"Please Enter your Name"
                 })
    email = forms.EmailField(label="Email", max_length=128)
    senha = forms.CharField(label="Senha" ,widget=forms.PasswordInput, min_length=8)
    senha2 = forms.CharField(label="digite a senha novamente" ,widget=forms.PasswordInput, min_length=8)

    def clean(self):
        self.cleaned_data = super().clean()
        pass1 = self.cleaned_data['senha']
        pass2 = self.cleaned_data['senha2']
        if pass1 != pass2:
            raise forms.ValidationError("Senhas não são iguais")

class LoginForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=64)
    senha = forms.CharField(label="Senha", min_length=8)