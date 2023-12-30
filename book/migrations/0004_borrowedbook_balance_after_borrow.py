# Generated by Django 4.2.7 on 2023-12-29 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_alter_book_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowedbook',
            name='balance_after_borrow',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
    ]
