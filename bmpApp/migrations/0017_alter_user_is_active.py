# Generated by Django 4.1.1 on 2024-02-13 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmpApp', '0016_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
