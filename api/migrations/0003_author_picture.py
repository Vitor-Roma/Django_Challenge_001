# Generated by Django 4.0.4 on 2022-05-19 20:38

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_article_author_alter_article_body_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.upload_image),
        ),
    ]
