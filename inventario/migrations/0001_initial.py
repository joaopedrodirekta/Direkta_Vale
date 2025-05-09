# Generated by Django 5.1.7 on 2025-03-27 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('categoria', models.CharField(blank=True, max_length=50, null=True)),
                ('quantidade', models.PositiveIntegerField(default=0)),
                ('local_armazenado', models.CharField(blank=True, max_length=100, null=True)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
