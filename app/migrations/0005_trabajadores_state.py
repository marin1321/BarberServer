# Generated by Django 3.2.9 on 2022-06-12 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_clientes_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajadores',
            name='state',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
