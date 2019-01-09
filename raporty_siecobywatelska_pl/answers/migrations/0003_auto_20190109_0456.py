# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-09 04:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutions', '0001_initial'),
        ('questionnaire', '0002_textoption'),
        ('answers', '0002_auto_20190106_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.Institution')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.TextOption')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Question')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('institution', 'question', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set([('institution', 'question')]),
        ),
    ]