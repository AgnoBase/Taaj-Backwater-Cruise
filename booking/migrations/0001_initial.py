# Generated by Django 4.1.6 on 2023-05-28 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('Duration1', models.IntegerField()),
                ('price1', models.IntegerField()),
                ('Duration2', models.IntegerField()),
                ('price2', models.IntegerField()),
                ('image', models.ImageField(upload_to='plan_img')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=20)),
                ('mname', models.CharField(max_length=10)),
                ('lname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=100)),
                ('cnum', models.IntegerField()),
                ('arrivedate', models.DateField()),
                ('adults', models.IntegerField()),
                ('child', models.IntegerField()),
                ('time', models.TimeField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.plans')),
            ],
        ),
    ]
