# Generated by Django 4.2.7 on 2023-12-30 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0007_remove_profile_user_profile_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='borrowed_book',
            field=models.ManyToManyField(to='book.borrowedbook'),
        ),
    ]
