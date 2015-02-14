# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('address_1', models.CharField(default=b'', max_length=200, blank=True)),
                ('address_2', models.CharField(default=b'', max_length=200, blank=True)),
                ('city', models.CharField(default=b'', max_length=200, blank=True)),
                ('state', models.CharField(default=b'', max_length=200, blank=True)),
                ('zip', models.CharField(default=b'', max_length=200, blank=True)),
                ('country', models.CharField(default=b'', max_length=200, blank=True)),
                ('phone', models.CharField(default=b'', max_length=200, blank=True)),
                ('picture', models.ImageField(upload_to=b'addr-book-photos', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Grumbls',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=400)),
                ('entry_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRelationship',
            fields=[
                ('user', models.OneToOneField(related_name=b'username_map', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('blockings', models.ManyToManyField(related_name=b'block_map', to=settings.AUTH_USER_MODEL)),
                ('followings', models.ManyToManyField(related_name=b'follow_map', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='grumbls',
            name='dislike_user',
            field=models.ManyToManyField(related_name=b'dislike_map', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='grumbls',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(to='grumblrApp.Grumbls'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
