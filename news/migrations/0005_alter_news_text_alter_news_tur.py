# Generated by Django 5.0.3 on 2024-05-03 06:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_news_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='text',
            field=models.TextField(verbose_name='Matn'),
        ),
        migrations.AlterField(
            model_name='news',
            name='tur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category', verbose_name='Yangilik Turi'),
        ),
    ]
