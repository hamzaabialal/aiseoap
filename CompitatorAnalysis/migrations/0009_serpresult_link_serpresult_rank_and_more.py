# Generated by Django 5.0.6 on 2024-06-29 04:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CompitatorAnalysis', '0008_alter_serpresult_keywords'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='serpresult',
            name='link',
            field=models.CharField(default=''),
        ),
        migrations.AddField(
            model_name='serpresult',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='serpresult',
            name='search_term',
            field=models.CharField(default=''),
        ),
        migrations.AddField(
            model_name='serpresult',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='serpresult',
            name='Keywords',
            field=models.CharField(default=''),
        ),
        migrations.AlterField(
            model_name='serpresult',
            name='query',
            field=models.CharField(max_length=255),
        ),
    ]
