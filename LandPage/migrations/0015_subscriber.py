# Generated by Django 2.1.3 on 2018-11-19 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandPage', '0014_auto_20181119_0701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(blank=True, max_length=128)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
