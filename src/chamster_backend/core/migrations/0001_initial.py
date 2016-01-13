# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(verbose_name=b'Event time stamp')),
                ('user', models.CharField(max_length=32)),
                ('comments', models.CharField(max_length=256, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('comments', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Event type',
                'verbose_name_plural': 'Event types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(verbose_name=b'Flow timestamp')),
                ('status', models.SmallIntegerField(verbose_name=b'Flow status')),
                ('comments', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['project', 'number'],
                'verbose_name': 'Flow',
                'verbose_name_plural': 'Flows',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_project', models.CharField(max_length=64)),
                ('work_project', models.CharField(max_length=128)),
                ('project_url', models.CharField(max_length=256)),
                ('comments', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['base_project', 'work_project', 'project_type'],
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('comments', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Project type',
                'verbose_name_plural': 'Project types',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.ForeignKey(verbose_name=b'Project type', to='core.ProjectType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('base_project', 'work_project')]),
        ),
        migrations.AddField(
            model_name='flow',
            name='project',
            field=models.ForeignKey(verbose_name=b'Project', to='core.Project'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='flow',
            unique_together=set([('project', 'number')]),
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(verbose_name=b'Event type', to='core.EventType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='event',
            name='flow',
            field=models.ForeignKey(verbose_name=b'Flow', to='core.Flow'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('flow', 'event_type', 'timestamp')]),
        ),
    ]
