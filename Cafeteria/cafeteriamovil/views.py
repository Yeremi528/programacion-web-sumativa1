from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User

from django.core.exceptions import ValidationError
from django.db import DataError
from django.db import IntegrityError

from django.urls import reverse



admin = "Administrador"
usuario = "usuario"

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def login(request):
    print("[LOGIN] got request method:", request.method)
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd   = request.POST.get('password')
        print(f"[LOGIN] Usuario: {email} — Contraseña: {pwd}")

        
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":

        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        account_type = request.POST.get("accountType")


        try:
            usuario = User.objects.create(
                name = name,
                lastname = lastname,
                email = email,
                password = password,
                account_type = account_type
            )

            if account_type == admin:
                return redirect("editaradmin")
            else:
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
    


def administrador(request):
    return render(request, 'adminuser.html')

def productos(request):
    return render(request, 'products.html')

def carrito(request):
    return render(request, 'cart.html')

def inventario(request):
    return render(request,'inventory.html')

def editaradmin(request):
    return render(request,'editprofileadmin.html')

def editaruser(request):
    return render(request, 'editprofileuser.html')