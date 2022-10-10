# Generated by Django 4.1.1 on 2022-10-10 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customername', models.CharField(max_length=50)),
                ('customerphone', models.CharField(max_length=50)),
                ('customeremail', models.CharField(max_length=50)),
                ('customeraddress', models.CharField(max_length=50)),
                ('paytype', models.CharField(default='ATM', max_length=5)),
            ],
        ),
    ]