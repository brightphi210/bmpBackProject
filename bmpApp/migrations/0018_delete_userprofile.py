# Generated by Django 4.1.1 on 2024-02-13 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bmpApp', '0017_alter_user_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
