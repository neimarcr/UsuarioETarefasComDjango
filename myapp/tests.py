from django.test import TestCase, Client
from tarefas.models import ListaTarefas
from django.contrib.auth.models import User


def logar_usuario():
    c = Client()
    c.login(username=User.objects.get(id=1).username, password=123)
    return c

# Create your tests here.

class TestTarefas(TestCase):

    def setUp(self) -> None:

        #Criar usuário
        user1 = User.objects.create_user(username="teste1", email="teste1@email.com", password="123")
        user2 = User.objects.create_user(username="teste2", email="teste2@email.com", password="321")

        #Criar tarefa
        tarefa1 = ListaTarefas.objects.create(nome="tarefa_1", usuario=user1, descricao="Fazer alguma coisa", realizada=True)
        tarefa2 = ListaTarefas.objects.create(nome="tarefa_2", usuario=user1, descricao="Fazer alguma outra coisa", realizada=False)    
        tarefa3 = ListaTarefas.objects.create(nome="tarefa_3", usuario=user2 ,descricao="Fazer alguma coisa diferente", realizada=True)


    # TESTES DE INSERÇÃO DE DADOS

    def test_descricao_salva_corretamente(self):
        t = ListaTarefas.objects.get(nome="tarefa_1")
        self.assertEqual(t.descricao, 'Fazer alguma coisa')

    def test_descricao_salva_corretamente_2(self):
        t = ListaTarefas.objects.get(nome="tarefa_1")
        self.assertNotEqual(t.descricao, 'Fazer alguma outra coisa')

    def test_realizada_salva_corretamente(self):
        t = ListaTarefas.objects.get(nome="tarefa_1")
        self.assertEqual(t.realizada, True) 

    def test_realizada_salva_corretamente_2(self):
        t = ListaTarefas.objects.get(nome="tarefa_2")
        self.assertEqual(t.realizada, False) 

    def test_usuario_salvo_corretamente(self):
        t = ListaTarefas.objects.get(nome="tarefa_3")
        u = User.objects.get(id=2)
        self.assertEqual(t.usuario, u)

    def test_usuario_salvo_corretamente_2(self):
        t = ListaTarefas.objects.get(nome="tarefa_3")
        u = User.objects.get(id=1)
        self.assertNotEqual(t.usuario, u)

    def test_senha_esta_cifrada(self):
        u = User.objects.get(id=1)
        self.assertNotEqual(u.password, '123')


    # TESTE DO CLIENTE, USUÁRIO NÃO LOGADO

    def test_pagina_inicial(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

    def test_pagina_cadastro_usuario(self):
        c = Client()
        response = c.get("/cadastrar_usuario")
        self.assertEqual(response.status_code, 200)

    def test_pagina_login(self):
        c = Client()
        response = c.get("/login_user")
        self.assertEqual(response.status_code, 200)
        u = User.objects.get(id=1)
        logged = c.login(username=u.username, password=123)
        self.assertTrue(logged)

    def test_pagina_tarefa_nao_logado(self):
        c = Client()
        response = c.get("/tarefas/")
        self.assertEqual(response.status_code, 302)

    def test_pagina_adicionar_tarefa_nao_logado(self):
        c = Client()
        response = c.get("/tarefas/adicionar")
        self.assertEqual(response.status_code, 302)

    def test_pagina_editar_tarefa_nao_logado(self):
        c = Client()
        t = ListaTarefas.objects.get(nome="tarefa_1")
        response = c.get(f"/tarefas/{t.id}/editar")
        self.assertEqual(response.status_code, 302)

    def test_pagina_deletar_tarefa_nao_logado(self):
        c = Client()
        t = ListaTarefas.objects.get(nome="tarefa_1")
        response = c.get(f"/tarefas/{t.id}/deletar_tarefa")
        self.assertEqual(response.status_code, 302)

    # TESTES COM USUÁRIO LOGADO

    def test_pagina_tarefa_logado(self):
        c = logar_usuario()
        response = c.get('/tarefas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lista'].count(), 2)

    def test_pagina_adicionar_tarefa_logado(self):
        c = logar_usuario()
        response = c.get('/tarefas/adicionar')
        self.assertEqual(response.status_code, 200)
        response = c.post('/tarefas/adicionar', {'nome': 'tarefa_4', 'descricao': 'testando', 'realizada': True})
        self.assertEqual(response.status_code, 302)
        t = ListaTarefas.objects.get(nome='tarefa_4')
        response = c.get('/tarefas/')
        self.assertIn(t, response.context['lista'])


    def test_pagina_editar_tarefa(self):
        c = logar_usuario()
        t = ListaTarefas.objects.get(nome="tarefa_1")        
        response = c.get(f'/tarefas/{t.id}/editar')
        self.assertEqual(response.status_code, 200)
        response = c.post(f'/tarefas/{t.id}/editar', {'nome': 'editando', 'descricao': 'testando', 'realizada': True})
        self.assertEqual(response.status_code, 302)
        t = ListaTarefas.objects.get(nome='editando')
        response = c.get('/tarefas/')
        self.assertIn(t, response.context['lista'])

    def test_deletar_tarefa_logado(self):
        c = logar_usuario()
        t = ListaTarefas.objects.get(nome="tarefa_1")        
        response = c.post(f'/tarefas/{t.id}/deletar_tarefa')
        self.assertEqual(response.status_code, 302)
        response = c.get('/tarefas/')
        self.assertNotIn(t ,response.context['lista'])


    # TESTES DE USUÁRIO ACESSANDO LISTA DE OUTRO USUÁRIO - É PROÍBIDO!

    def test_acessar_lista_outro_user(self):
        c = logar_usuario()
        t = ListaTarefas.objects.get(nome="tarefa_3")        
        response = c.get('/tarefas/')
        self.assertNotIn(t ,response.context['lista'])

    def test_editar_lista_outro_user(self):
        c = logar_usuario()
        t = ListaTarefas.objects.get(nome="tarefa_3")        
        response = c.get(f'/tarefas/{t.id}/editar')
        self.assertEqual(response.status_code, 403)
        

    def test_deletar_tarefa_outro_user(self):
        c = logar_usuario()
        t = ListaTarefas.objects.get(nome="tarefa_3")        
        response = c.post(f'/tarefas/{t.id}/deletar_tarefa')
        self.assertEqual(response.status_code, 403)
        t = ListaTarefas.objects.get(nome="tarefa_3")        
        self.assertTrue(t)

        