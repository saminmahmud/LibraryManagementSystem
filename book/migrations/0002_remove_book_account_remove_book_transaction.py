# Generated by Django 4.2.7 on 2023-12-29 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='account',
        ),
        migrations.RemoveField(
            model_name='book',
            name='transaction',
        ),
    ]
