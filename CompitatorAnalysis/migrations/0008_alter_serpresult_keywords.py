# Generated by Django 5.0.6 on 2024-06-26 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompitatorAnalysis', '0007_alter_serpresult_keywords'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serpresult',
            name='Keywords',
            field=models.JSONField(),
        ),
    ]
