# Generated by Django 3.1.7 on 2021-04-19 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-id',), 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
    ]