# Generated by Django 4.1.1 on 2024-03-09 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bmpApp', '0021_skills_userprofile_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='skill',
        ),
        migrations.DeleteModel(
            name='Skills',
        ),
    ]
