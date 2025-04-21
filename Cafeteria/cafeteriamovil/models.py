from django.db import models

# Usuario
class Usuario(models.Model):
    name = models.CharField("Nombre", max_length=255)
    lastname = models.CharField("Apellido", max_length=255)
    email = models.EmailField("Correo Electrónico", unique=True)
    password = models.CharField("Contraseña", max_length=255)
    account_type = models.CharField("Tipo de Cuenta", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.lastname}"


# Cliente
class Client(models.Model):
    nombre_cliente = models.CharField("Nombre", max_length=255)
    correo_cliente = models.EmailField("Correo electrónico", unique=True)
    contraseña_cliente = models.CharField("Contraseña", max_length=255)
    direccion_cliente = models.CharField("Dirección", max_length=255)
    telefono_cliente = models.BigIntegerField("Teléfono")
    fecha_registro = models.DateField("Fecha de registro")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre_cliente} - {self.correo_cliente}"


# Stock
class Stock(models.Model):
    cantidad_disp = models.IntegerField("Cantidad disponible")
    unidad_medida = models.CharField("Unidad de medida", max_length=2)
    fecha_actualizacion = models.DateField("Fecha de actualización")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock #{self.id} - {self.cantidad_disp} {self.unidad_medida}"


# Producto
class Product(models.Model):
    nombre_product = models.CharField("Nombre", max_length=255)
    descripcion_product = models.TextField("Descripción")
    precio_product = models.PositiveIntegerField("Precio")
    tipo_product = models.CharField("Tipo", max_length=255)
    imagen_product = models.BinaryField("Imagen", blank=True, null=True)
    stock_stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="productos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre_product


# Promociones
class Promotions(models.Model):
    titulo_promocion = models.CharField("Título", max_length=255)
    descripcion = models.TextField("Descripción")
    fecha_inicio = models.DateField("Inicio")
    fecha_termino = models.DateField("Término")
    imagen_promocion = models.BinaryField("Imagen", blank=True, null=True)

    def __str__(self):
        return self.titulo_promocion


# Pedido
class Order(models.Model):
    fecha_pedido = models.DateField("Fecha")
    total_pedido = models.CharField("Total", max_length=255)
    estado_pedido = models.CharField("Estado", max_length=255)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="pedidos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.client.nombre_cliente}"


# Detalle del pedido
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="detalles")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="detalles_pedido")
    cantidad = models.PositiveIntegerField("Cantidad")
    subtotal = models.PositiveIntegerField("Subtotal")

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"{self.order} - {self.product.nombre_product}"


# Reseñas
class Reviews(models.Model):
    comentarios = models.TextField("Comentarios")
    calificacion = models.CharField("Calificación", max_length=255)
    fecha = models.DateField("Fecha")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reseñas")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reseñas")

    def __str__(self):
        return f"Reseña de {self.client.nombre_cliente} sobre {self.product.nombre_product}"