# Generated by Django 4.1.5 on 2023-02-01 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0010_alter_reply_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='text',
            field=models.TextField(),
        ),
    ]
