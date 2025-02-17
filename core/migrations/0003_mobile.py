# Generated by Django 5.0.1 on 2024-03-11 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_userprofile_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('selling_price', models.IntegerField()),
                ('mobile_image', models.ImageField(upload_to='mobile_images')),
                ('display', models.CharField(max_length=100)),
                ('processor', models.CharField(max_length=100)),
                ('ram', models.CharField(max_length=100)),
                ('storage', models.CharField(max_length=100)),
                ('camera', models.CharField(max_length=100)),
                ('battery', models.CharField(max_length=100)),
            ],
        ),
    ]
