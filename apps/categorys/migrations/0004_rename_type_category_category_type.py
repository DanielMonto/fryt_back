# Generated by Django 5.0.4 on 2024-05-20 00:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categorys', '0003_remove_category_types_category_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='type',
            new_name='category_type',
        ),
    ]
