# Generated by Django 3.2.6 on 2021-08-29 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=355)),
                ('username', models.CharField(max_length=50)),
                ('image_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='matches',
            field=models.ManyToManyField(blank=True, to='users.MetaProfile'),
        ),
    ]
