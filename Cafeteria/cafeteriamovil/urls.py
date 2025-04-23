from django.urls import path
from .views import inicio, login, signup, usuario, carrito, inventario, productos, editaruser, password_reset
urlpatterns = [
    path('', inicio, name="inicio"),
    path('inicio', inicio, name="inicio"),
    path('inicio/login/', login, name="login"),
    path('inicio/signup', signup, name="signup"),
    path('usuario/<int:usuario_id>/', usuario, name="usuario"),
    path('productos', productos, name="productos"),
    path('productos/carrito', carrito, name="carrito"),
    path('administrador/inventario', inventario, name="inventario"),
    path('usuario/<int:usuario_id>/editar', editaruser, name="editaruser"),
    path('password-reset/', password_reset, name='password_reset'),

]
