# Generated by Django 5.0.4 on 2024-06-05 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='name',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
