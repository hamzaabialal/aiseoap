# Generated by Django 5.0.6 on 2024-06-29 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompitatorAnalysis', '0011_serpresult_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='serpresult',
            name='image',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
