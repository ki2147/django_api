# Generated by Django 4.2.2 on 2023-06-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productapp', '0003_delete_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=60)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]
