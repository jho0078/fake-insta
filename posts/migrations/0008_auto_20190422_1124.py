# Generated by Django 2.1.8 on 2019-04-22 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_post_like_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(blank=True, to='posts.Hashtag'),
        ),
    ]
