# Generated by Django 5.0.1 on 2024-03-15 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='pet',
            new_name='mobile',
        ),
    ]
