# Generated by Django 4.1.1 on 2022-09-14 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cls', models.CharField(max_length=2)),
                ('eng', models.CharField(max_length=100)),
                ('jpn', models.CharField(max_length=100)),
                ('ruijigun', models.CharField(max_length=6)),
                ('nice', models.CharField(max_length=6)),
            ],
        ),
    ]
