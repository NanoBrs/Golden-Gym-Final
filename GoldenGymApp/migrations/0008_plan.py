# Generated by Django 3.2 on 2024-11-22 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoldenGymApp', '0007_alter_cliente_suscripcion_activa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('precio', models.IntegerField()),
                ('duracion_dias', models.IntegerField()),
            ],
        ),
    ]