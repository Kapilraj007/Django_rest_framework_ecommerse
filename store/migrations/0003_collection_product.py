# Generated by Django 5.0.3 on 2024-03-20 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_customer_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('stock', models.PositiveSmallIntegerField()),
                ('description', models.TextField()),
                ('vendor', models.CharField(max_length=255)),
                ('price', models.PositiveIntegerField()),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.collection')),
            ],
        ),
    ]
