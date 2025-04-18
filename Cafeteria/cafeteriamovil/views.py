from django.shortcuts import render

# Create your views here.
def inicio(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def usuario(request):
    return render(request, 'user.html')

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