# Generated by Django 3.2 on 2024-11-06 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoldenGymApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encargado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('correo', models.EmailField(max_length=100, unique=True)),
                ('usuario', models.CharField(max_length=50, unique=True)),
                ('contraseña', models.CharField(max_length=100)),
            ],
        ),
    ]