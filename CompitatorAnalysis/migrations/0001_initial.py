# Generated by Django 5.0.6 on 2024-06-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SerpResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('display_link', models.CharField(max_length=255)),
                ('rank', models.IntegerField()),
            ],
        ),
    ]
