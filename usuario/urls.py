from django.urls import path
from usuario import views

app_name = 'usuario'

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastrar_usuario", views.cadastrar_usuario, name="cadastrar_usuario"),
    path("login_user", views.login_user, name="login_user"),
    path("logout_user", views.logout_user, name="logout_user"),
]