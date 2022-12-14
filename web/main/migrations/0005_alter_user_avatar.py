# Generated by Django 4.1.2 on 2022-12-14 15:38

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=main.models.upload_avatar_path),
        ),
    ]
