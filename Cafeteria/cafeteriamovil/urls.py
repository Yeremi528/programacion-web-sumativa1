from django.urls import path
from .views import inicio, login, signup, usuario, administrador, carrito, inventario, productos, editaradmin, editaruser
urlpatterns = [
    path('inicio', inicio, name="inicio"),
    path('inicio/login/', login, name="login"),
    path('inicio/signup', signup, name="signup"),
    path('usuario/<int:usuario_id>/', usuario, name="usuario"),
    path('administrador', administrador, name="administrador"),
    path('productos', productos, name="productos"),
    path('productos/carrito', carrito, name="carrito"),
    path('administrador/inventario', inventario, name="inventario"),
    path('administrador/editar', editaradmin, name="editaradmin"),
    path('usuario/editar', editaruser, name="editaruser")
]
