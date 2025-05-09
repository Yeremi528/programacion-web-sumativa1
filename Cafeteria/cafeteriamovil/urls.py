from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import inicio,usuario_api, order_api, login, signup, usuario, carrito, inventario, productos, editaruser, password_reset, ProductViewSet
from . import views
from django.conf import settings
from django.conf.urls.static import static
#Router de Django REST Framework para generar rutas automáticas del CRUD
router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', inicio, name="inicio"),
    path('inicio', inicio, name="inicio"),
    path('inicio/login/', login, name="login"),
    path('inicio/signup', signup, name="signup"),
    path('usuario/', usuario, name="usuario"),
    path('productos/', productos, name="productos"),
    path('productos/carrito/', carrito, name="carrito"),
    path('administrador/inventario/', inventario, name="inventario"),
    path('usuario/editar', editaruser, name="editaruser"),
    path('password-reset/', password_reset, name='password_reset'),
    path("api/usuario/", usuario_api, name="usuario_api"),
    path("api/order/", order_api, name="order_api"),

    # se agrega esta linea para exponer las rutas de la API
    path('api/', include(router.urls)),
    path('api/productos/', views.ListCreateProduct.as_view(), name='productos_list_create'),
    path('api/productos/<int:id>/', views.RetrieveUpdateDestroyProduct.as_view(), name='productos_retrieve_update_destroy'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)