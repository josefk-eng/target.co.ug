# Generated by Django 4.1.6 on 2023-03-17 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('token', models.CharField(max_length=1000)),
                ('deviceId', models.CharField(max_length=500, primary_key=True, serialize=False)),
                ('isActive', models.BooleanField(default=True)),
                ('address', models.CharField(default='', max_length=1000)),
                ('phoneNumber', models.CharField(default='', max_length=20)),
                ('name', models.CharField(default='', max_length=500)),
                ('email', models.CharField(default='', max_length=300)),
                ('password', models.CharField(default='', max_length=300)),
                ('dateAdded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
