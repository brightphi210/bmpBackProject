# Generated by Django 4.1.1 on 2024-02-01 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bmpApp', '0005_alter_user_is_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auto_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
