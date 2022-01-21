# Generated by Django 3.2.8 on 2022-01-03 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20211227_1222'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='review',
            field=models.TextField(blank=True),
        ),
    ]