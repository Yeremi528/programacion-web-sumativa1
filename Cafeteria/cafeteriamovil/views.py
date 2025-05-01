from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User,Account_Detail, Product, Order,OrderDetail

import jwt
import os
import json

from datetime import datetime, timedelta, timezone


from django.http import JsonResponse


from django.core.exceptions import ValidationError
from django.db import DataError
from django.db import IntegrityError

from django.contrib.auth.hashers import check_password

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed


admin = "admin"
usuario = "usuario"


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

private_key_path = os.path.join(BASE_DIR,  'keys', 'private_key.pem')
with open(private_key_path, 'r') as file:
    private_key = file.read()


public_key_path = os.path.join(BASE_DIR, 'keys', 'public_key.pem')
with open(public_key_path, 'r') as file:
    public_key = file.read()


    
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

            now = datetime.now(timezone.utc)
            exp = now + timedelta(days=365)

            payload = {
                "ID": usuario.id,
                "exp": exp,
                "iat": now,
            }

            token = jwt.encode(payload, private_key, algorithm='RS256')
        except User.DoesNotExist:
            error = "Usuario no encontrado"
            return render(request, "login.html", {"error": error})

        if usuario.password != pwd:
            error = "Contraseña incorrecta"
            return render(request, "login.html", {"error": error})

        return render(request, "token_redirect.html", {"token": token})

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        account_type = request.POST.get("accountType")

        account_type_instance, created = Account_Detail.objects.get_or_create(account_type=account_type)

        try:
            if User.objects.filter(email=email).exists():
                error = "Usuario ya existente"
                return render(request, "signup.html", {"error": error})
            
            usuario = User(
                name=name,
                lastname=lastname,
                email=email,
                password=password, 
                account_type=account_type_instance
            )
            usuario.save()

            now = datetime.now(timezone.utc)
            exp = now + timedelta(days=365)


            payload = {
                "ID": usuario.id,
                "exp": exp,
                "iat": now,
            }

            token = jwt.encode(payload, private_key, algorithm='RS256')

            return render(request, "token_redirect.html", {"token": token})

        except IntegrityError:
            return HttpResponse("Error: El correo ya existe o hay campos obligatorios vacíos.")
        except DataError:
            return HttpResponse("Error: Uno de los campos tiene un valor no válido o demasiado largo.")
        except ValidationError as e:
            return HttpResponse(f"Error de validación: {e}")
        except Exception as e:
            return HttpResponse(f"Ocurrió un error inesperado: {e}")

    return render(request, 'signup.html')


@csrf_exempt
def usuario_api(request):
    token = request.headers.get('Authorization', '')
    if not token:
        return JsonResponse({"error": "Token no enviado"}, status=401)

    try:
        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        usuario_id = decoded.get("ID")
    except Exception as e:
        return JsonResponse({"error": f"Token inválido: {str(e)}"}, status=400)

    if request.method == 'GET':
        try:
            usuario = User.objects.get(id=usuario_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)

        return JsonResponse({
            "name": usuario.name,
            "lastname": usuario.lastname,
            "email": usuario.email,
            "account_type": usuario.account_type.account_type,
            "id": usuario.id
        })

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)

        try:
            usuario = User.objects.get(id=usuario_id)

            usuario.name = data.get("name", usuario.name)
            usuario.email = data.get("email", usuario.email)
            
            usuario.save()

        except User.DoesNotExist:
            return JsonResponse({"error": "Usuario no encontrado"}, status=404)


        return JsonResponse({
            "success": True,
            "message": "Perfil actualizado",
            "name": usuario.name,
            "email": usuario.email,
        })



@csrf_exempt
def order_api(request):
    # Para obtenerlos desde el carrito
    token = request.headers.get('Authorization', '')
    if request.method == 'GET':

        decoded = jwt.decode(token, public_key, algorithms=["RS256"])
        usuario_id = decoded.get("ID")
        usuario = User.objects.get(id=usuario_id)
        
        detalles = OrderDetail.objects.select_related('order', 'product') \
        .filter(order__client=usuario)

        print(detalles)
       
    elif request.method == 'POST':
        try:
            decoded = jwt.decode(token, public_key, algorithms=["RS256"])
            usuario_id = decoded.get("ID")

            data = json.loads(request.body)

            producto = Product(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                stock=data['stock'],
                usuario=User.objects.get(id=usuario_id),
            )
            producto.save()


            return JsonResponse({"success": True, "message": "Producto creado"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except KeyError:
            return JsonResponse({"error": "Faltan campos requeridos"}, status=400)
    # Acciones desde el carrito
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            producto = Product.objects.get(id=data['id'])
            producto.name = data.get('name', producto.name)
            producto.description = data.get('description', producto.description)
            producto.price = data.get('price', producto.price)
            producto.stock = data.get('stock', producto.stock)
            producto.save()
            return JsonResponse({"success": True, "message": "Producto actualizado"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "JSON inválido"}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)


def usuario(request):
    return render(request, "user.html") 


def productos(request):
    productos = Product.objects.all()
    return render(request, 'products.html', {'productos': productos})

def carrito(request):
    return render(request, 'cart.html')

def inventario(request):
    return render(request,'inventory.html')


def editaruser(request):
    return render(request, 'editprofileuser.html')

def recetas(request):
    return render(request, 'recetas.html')

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
