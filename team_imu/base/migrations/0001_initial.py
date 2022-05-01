# Generated by Django 2.2.9 on 2020-01-26 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_name', models.CharField(max_length=50, verbose_name='IMAGE NAME')),
                ('img_type', models.CharField(choices=[('STANDARD', 'STANDARD'), ('EMERGENT', 'EMERGENT')], max_length=15)),
                ('img', models.ImageField(upload_to='media/results')),
                ('shape', models.CharField(choices=[('NONE', 'NONE'), ('CIRCLE', 'CIRCLE'), ('SEMICIRCLE', 'SEMICIRCLE'), ('QUARTER_CIRCLE', 'QUARTER_CIRCLE'), ('TRIANGE', 'TRIANGLE'), ('SQUARE', 'SQUARE'), ('RECTANGLE', 'RECTANGLE'), ('TRAPEZOID', 'TRAPEZOID'), ('PENTAGON', 'PENTAGON'), ('HEXAGON', 'HEXAGON'), ('HEPTAGON', 'HEPTAGON'), ('OCTAGON', 'OCTAGON'), ('STAR', 'STAR'), ('CROSS', 'CROSS')], max_length=20)),
                ('shape_color', models.CharField(choices=[('WHITE', 'WHITE'), ('BLACK', 'BLACK'), ('RED', 'RED'), ('YELLOW', 'YELLOW'), ('GRAY', 'GRAY'), ('GREEN', 'GREEN'), ('PURPLE', 'PURPLE'), ('BROWN', 'BROWN'), ('BLUE', 'BLUE'), ('ORANGE', 'ORANGE')], max_length=15)),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('orientation', models.CharField(choices=[('N', 'N'), ('W', 'W'), ('E', 'E'), ('S', 'S'), ('NE', 'NE'), ('SE', 'SE'), ('SW', 'SW'), ('NW', 'NW')], max_length=2)),
                ('alphanumeric', models.CharField(max_length=2)),
                ('alphanumeric_color', models.CharField(choices=[('WHITE', 'WHITE'), ('BLACK', 'BLACK'), ('RED', 'RED'), ('YELLOW', 'YELLOW'), ('GRAY', 'GRAY'), ('GREEN', 'GREEN'), ('PURPLE', 'PURPLE'), ('BROWN', 'BROWN'), ('BLUE', 'BLUE'), ('ORANGE', 'ORANGE')], max_length=20)),
                ('is_autonom', models.CharField(choices=[('A', 'AUTONOMOUS'), ('M', 'MANUEL')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Team ID')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('name', models.CharField(max_length=50, verbose_name='Team Username')),
                ('university', models.CharField(max_length=50, verbose_name='Unıversity Name')),
                ('InAir', models.BooleanField()),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('altitude', models.FloatField(verbose_name='Altitude')),
                ('heading', models.FloatField(verbose_name='Heading')),
                ('telemetry_id', models.IntegerField(verbose_name='Telemetry ID')),
                ('telemetry_age_sec', models.FloatField()),
                ('telemetry_time_stamp', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Telemetry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('altitude', models.FloatField(verbose_name='Altitude')),
                ('heading', models.FloatField(verbose_name='Heading')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='User ID')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('password', models.CharField(max_length=50, verbose_name='Password')),
                ('confirm_password', models.CharField(max_length=50, verbose_name='Confirm Password')),
            ],
        ),
    ]