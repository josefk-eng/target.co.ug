# Generated by Django 4.1.6 on 2023-02-11 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=500)),
                ('caption', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='img/banners')),
                ('tags', models.CharField(default='', max_length=1000)),
                ('isMain', models.BooleanField(default=False)),
                ('buttonAlign', models.CharField(default='left', max_length=20)),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(default='', max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, default='default.png', upload_to='img/cats')),
                ('availability', models.BooleanField(default=False)),
                ('ui', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categorys',
            },
        ),
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csv/')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('is_activated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('isActive', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Season',
                'verbose_name_plural': 'Seasons',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('stockId', models.BigIntegerField(default=0)),
                ('serialNumber', models.BigIntegerField(default=0)),
                ('name', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('cost_price', models.IntegerField(default=0.0)),
                ('price', models.IntegerField(default=0.0)),
                ('department', models.CharField(max_length=200)),
                ('image', models.ImageField(default='default.png', upload_to='products/')),
                ('availability', models.BooleanField(default=False)),
                ('unit', models.CharField(default='kg', max_length=20)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('tag', models.CharField(default='untagged', max_length=100)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(default='Sales', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employee',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.season'),
        ),
    ]
