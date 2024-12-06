# Generated by Django 5.1.2 on 2024-11-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_devisdemande_fireplace_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devisdemande',
            old_name='color_scheme',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='devisdemande',
            name='description',
        ),
        migrations.RemoveField(
            model_name='devisdemande',
            name='fireplace_type',
        ),
        migrations.RemoveField(
            model_name='devisdemande',
            name='height',
        ),
        migrations.RemoveField(
            model_name='devisdemande',
            name='width',
        ),
        migrations.AddField(
            model_name='devisdemande',
            name='address',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='devisdemande',
            name='governorate',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='devisdemande',
            name='phone',
            field=models.CharField(default='00000000', max_length=8),
        ),
    ]
