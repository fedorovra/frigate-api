# Generated by Django 3.1.7 on 2021-03-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIKeys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=25, unique=True)),
                ('permissions', models.CharField(blank=True, max_length=250, null=True)),
                ('is_active', models.CharField(default='Y', max_length=1)),
            ],
        ),
    ]