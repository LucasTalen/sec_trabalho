# Generated by Django 5.0.7 on 2024-07-28 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_sec', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='foto_perfil',
            field=models.ImageField(default='', upload_to='profile_images/'),
            preserve_default=False,
        ),
    ]
