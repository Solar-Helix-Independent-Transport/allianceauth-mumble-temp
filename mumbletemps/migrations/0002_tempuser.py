# Generated by Django 2.2.12 on 2020-06-04 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mumbletemps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('expires', models.IntegerField()),
            ],
        ),
    ]