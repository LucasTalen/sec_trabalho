# Generated by Django 5.0.7 on 2024-08-10 01:14
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_sec', '0003_extrasfuncionario'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='admissao',
            field=models.DateField(default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
