# Generated by Django 3.0.3 on 2020-02-07 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20200207_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='img',
        ),
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(upload_to='result'),
        ),
    ]