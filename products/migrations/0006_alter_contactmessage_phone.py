# Generated by Django 5.1.2 on 2024-11-06 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_contactmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='phone',
            field=models.CharField(default='00000000', max_length=8),
        ),
    ]