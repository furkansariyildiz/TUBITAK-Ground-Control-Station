# Generated by Django 3.0 on 2020-02-17 19:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20200207_2007'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Photo',
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'verbose_name': 'photo', 'verbose_name_plural': 'photos'},
        ),
        migrations.AddField(
            model_name='result',
            name='description',
            field=models.CharField(blank=True, max_length=225, verbose_name='Açıklama'),
        ),
        migrations.AddField(
            model_name='result',
            name='file',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='result'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
