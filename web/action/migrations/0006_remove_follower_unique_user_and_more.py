# Generated by Django 4.1.4 on 2023-01-28 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0005_alter_follower_options_alter_follower_follower'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follower',
            name='unique_user',
        ),
        migrations.AddConstraint(
            model_name='follower',
            constraint=models.UniqueConstraint(fields=('follower', 'content_maker'), name='unique_following'),
        ),
    ]
