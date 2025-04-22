from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User,Account_Detail,Product

from django.core.exceptions import ValidationError
from django.db import DataError
from django.db import IntegrityError

from django.contrib.auth.hashers import check_password



admin = "Administrador"
usuario = "usuario"

def password_reset(request):
    if request.method == "POST":
        error = None

        email = request.POST.get('email')
        pwd = request.POST.get('password') 

        print(email)
        print(pwd)

        try:
            usuario = User.objects.get(email=email)
            usuario.password = pwd
            usuario.save()

        except User.DoesNotExist:
            error = "Usuario no encontrado"
            return render(request, "password_reset.html", {"error": error})

        if usuario.account_type == admin:
            return redirect("editaradmin")
        else:
            return redirect("usuario", usuario.id)

    return render(request, 'password_reset.html')

def inicio(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        error = None

        email = request.POST.get('email')
        pwd = request.POST.get('password')

        print(email)
        print(pwd)

      
        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            error = "Usuario no encontrado"
            return render(request, "login.html", {"error": error})

        if usuario.password != pwd:
            error = "Contraseña incorrecta"
            return render(request, "login.html", {"error": error})

        if usuario.account_type == admin:
            return redirect("editaradmin")
        else:
            return redirect("usuario", usuario.id)

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":

        name = request.POST.get("name")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        account_type = request.POST.get("accountType")

        account_type_instance, created = Account_Detail.objects.get_or_create(account_type=account_type)

        print(created)

        try:
            usuario = User.objects.create(
                name = name,
                lastname = lastname,
                email = email,
                password = password,
                account_type=account_type_instance
                 
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
    productos = Product.objects.all()
    return render(request, 'products.html', {'productos': productos})

def carrito(request):
    return render(request, 'cart.html')

def inventario(request):
    return render(request,'inventory.html')

def editaradmin(request):
    return render(request,'editprofileadmin.html')

def editaruser(request):
    return render(request, 'editprofileuser.html')