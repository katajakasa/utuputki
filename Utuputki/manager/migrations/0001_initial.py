# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SkipRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=64, verbose_name='Sender Key')),
            ],
            options={
                'verbose_name': 'Skip request',
                'verbose_name_plural': 'Skip requests',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text='Description text for the video', verbose_name='Description', blank=True)),
                ('youtube_url', models.URLField(help_text='URL to a youtube video', verbose_name='Youtube URL')),
                ('key', models.CharField(max_length=64, null=True, verbose_name='Sender Key', blank=True)),
                ('deleted', models.IntegerField(default=False, verbose_name='Deleted')),
                ('playing', models.BooleanField(default=False, verbose_name='Playing')),
                ('duration', models.IntegerField(default=0, verbose_name='Duration')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='skiprequest',
            name='event',
            field=models.ForeignKey(verbose_name='Video', to='manager.Video'),
            preserve_default=True,
        ),
    ]
