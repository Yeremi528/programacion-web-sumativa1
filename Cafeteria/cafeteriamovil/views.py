from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User,Account_Detail, Product

from django.core.exceptions import ValidationError
from django.db import DataError
from django.db import IntegrityError

from django.contrib.auth.hashers import check_password

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer

admin = "admin"
usuario = "usuario"

def password_reset(request):
    if request.method == "POST":
        error = None

        email = request.POST.get('email')
        pwd = request.POST.get('password') 

        try:
            usuario = User.objects.get(email=email)
            usuario.password = pwd
            usuario.save()

        except User.DoesNotExist:
            error = "Usuario no encontrado"
            return render(request, "password_reset.html", {"error": error})

         
        return redirect("usuario", usuario.id)

    return render(request, 'password_reset.html')

def inicio(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        error = None

        email = request.POST.get('email')
        pwd = request.POST.get('password')

      
        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            error = "Usuario no encontrado"
            return render(request, "login.html", {"error": error})

        if usuario.password != pwd:
            error = "Contraseña incorrecta"
            return render(request, "login.html", {"error": error})

      
        return redirect("usuario", usuario.id)

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        account_type = request.POST.get("accountType")

        print(account_type)
        account_type_instance, created = Account_Detail.objects.get_or_create(account_type=account_type)
        print(account_type_instance)

        try:
            if User.objects.filter(email=email).exists():
                error = "Usuario ya existente"
                return render(request, "signup.html", {"error": error})
            
            usuario = User.objects.create(
                name=name,
                lastname=lastname,
                email=email,
                password=password, 
                account_type=account_type_instance
            )


            return redirect("usuario", usuario.id)

        except IntegrityError:
            return HttpResponse("Error: El correo ya existe o hay campos obligatorios vacíos.")
        except DataError:
            return HttpResponse("Error: Uno de los campos tiene un valor no válido o demasiado largo.")
        except ValidationError as e:
            return HttpResponse(f"Error de validación: {e}")
        except Exception as e:
            return HttpResponse(f"Ocurrió un error inesperado: {e}")

    return render(request, 'signup.html')
def usuario(request, usuario_id):
    try:
        usuario = User.objects.get(id=usuario_id)
        return render(request, 'user.html', {"usuario": usuario})

    except User.DoesNotExist:
        return HttpResponse("No se encontró un usuario con ese correo.")
    except User.MultipleObjectsReturned:
        return HttpResponse("Error: hay múltiples usuarios con ese correo.")
    



def productos(request):
    productos = Product.objects.all()
    return render(request, 'products.html', {'productos': productos})

def carrito(request):
    return render(request, 'cart.html')

def inventario(request):
    return render(request,'inventory.html')


def editaruser(request,usuario_id):
    try:
        usuario = User.objects.get(id=usuario_id)
        return render(request, 'editprofileuser.html', {"usuario":usuario})
    except User.DoesNotExist:
        return HttpResponse("No se encontró un usuario con ese correo.")
    except User.MultipleObjectsReturned:
        return HttpResponse("Error: hay múltiples usuarios con ese correo.")


# ViewSet crea automaticamente endpoints para listar, crear, editar y eliminar productos
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')  # Trae los productos ordenados por fecha de creacion
    serializer_class = ProductSerializer  # Usamos el serializer que creamos en serializers.py

# Listar y crear productos
class ListCreateProduct(APIView):
    def get(self, request):
        productos = Product.objects.all()
        serializer = ProductSerializer(productos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Ver, editar y eliminar un producto
class RetrieveUpdateDestroyProduct(APIView):
    def get(self, request, id):
        try:
            producto = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(producto)
        return Response(serializer.data)

    def put(self, request, id):
        try:
            producto = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            producto = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
