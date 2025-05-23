# Generated by Django 5.2 on 2025-05-11 00:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeteriamovil', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField(verbose_name='Fecha')),
                ('order_total', models.CharField(max_length=255, verbose_name='Total')),
                ('order_status', models.CharField(max_length=255, verbose_name='Estado')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Cantidad')),
                ('subtotal', models.PositiveIntegerField(verbose_name='Subtotal')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='cafeteriamovil.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('product_desc', models.TextField(verbose_name='Descripción')),
                ('product_price', models.PositiveIntegerField(verbose_name='Precio')),
                ('stock_product', models.PositiveIntegerField(verbose_name='Stock')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('imagen_product', models.ImageField(blank=True, null=True, upload_to='productos/', verbose_name='Imagen')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_title', models.CharField(max_length=255, verbose_name='Título')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('start_time', models.DateField(verbose_name='Inicio')),
                ('end_time', models.DateField(verbose_name='Término')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentarios', models.TextField(verbose_name='Comentarios')),
                ('calificacion', models.CharField(max_length=255, verbose_name='Calificación')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas', to='cafeteriamovil.product')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre')),
                ('lastname', models.CharField(max_length=255, verbose_name='Apellido')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('password', models.CharField(max_length=255, verbose_name='Contraseña')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to='cafeteriamovil.account_detail')),
            ],
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_pedido', to='cafeteriamovil.product'),
        ),
        migrations.AddField(
            model_name='reviews',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reseñas', to='cafeteriamovil.user'),
        ),
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='cafeteriamovil.user'),
        ),
        migrations.AlterUniqueTogether(
            name='orderdetail',
            unique_together={('order', 'product')},
        ),
    ]
