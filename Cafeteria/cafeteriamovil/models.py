from django.db import models
# Tipo Cuenta
class Account_Detail(models.Model):
    account_type = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.account_type


# Usuario
class User(models.Model):
    ID = models.CharField("ID", max_length=255)
    name = models.CharField("Nombre", max_length=255)
    lastname = models.CharField("Apellido", max_length=255)
    email = models.EmailField("Correo Electrónico", unique=True)
    password = models.CharField("Contraseña", max_length=255)
    account_type = models.ForeignKey(Account_Detail, on_delete=models.CASCADE, related_name="usuario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.lastname}"


# Promociones
class Promotions(models.Model):
    promotion_title = models.CharField("Título", max_length=255)
    description = models.TextField("Descripción")
    start_time = models.DateField("Inicio")
    end_time = models.DateField("Término")
    promotional_image = models.BinaryField("Imagen", blank=True, null=True)

    def __str__(self):
        return self.promotion_title


# Tipo Producto
class Product_Detail(models.Model):
    product_type = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.product_type


# Producto
class Product(models.Model):
    product_name = models.CharField("Nombre", max_length=255)
    product_desc = models.TextField("Descripción")
    product_price = models.PositiveIntegerField("Precio")
    stock_product = models.PositiveIntegerField("Stock")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # promotion = models.ForeignKey(Promotions, on_delete=models.CASCADE, related_name="promocion")
    # imagen_product = models.BinaryField("Imagen", blank=True, null=True)
    # product_type = models.ForeignKey(Product_Detail, on_delete=models.CASCADE, related_name="tipo_producto", default=1)

    def str(self):
        return self.product_name


# Pedido
class Order(models.Model):
    order_date = models.DateField("Fecha")
    order_total = models.CharField("Total", max_length=255)
    order_status = models.CharField("Estado", max_length=255)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pedidos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - Cliente: {self.client.name} {self.client.lastname}"


# Detalle del pedido
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="detalles")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="detalles_pedido")
    quantity = models.PositiveIntegerField("Cantidad")
    subtotal = models.PositiveIntegerField("Subtotal")

    class Meta:
        unique_together = (('order', 'product'),)

    def __str__(self):
        return f"{self.order} - {self.product.product_name}"


# Reseñas
class Reviews(models.Model):
    comentarios = models.TextField("Comentarios")
    calificacion = models.CharField("Calificación", max_length=255)
    fecha = models.DateField("Fecha")
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reseñas")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reseñas")

    def __str__(self):
        return f"Reseña de {self.client.name} {self.client.lastname} sobre {self.product.product_name}"