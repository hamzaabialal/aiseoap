# Generated by Django 5.0.6 on 2024-06-29 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CompitatorAnalysis', '0014_rename_keywords_serpresult_keywords_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='serpresult',
            old_name='image',
            new_name='link',
        ),

        migrations.RemoveField(
            model_name='serpresult',
            name='created_at',
        ),

    ]
