# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-21 10:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flow', '0003_data_dependency_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='datadependency',
            name='kind',
            field=models.CharField(choices=[('io', 'Input/output dependency'), ('subprocess', 'Subprocess')], default='io', max_length=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='datadependency',
            name='child',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parents_dependency', to='flow.Data'),
        ),
        migrations.AlterField(
            model_name='datadependency',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children_dependency', to='flow.Data'),
        ),
        migrations.AlterModelTable(
            name='datadependency',
            table=None,
        ),
    ]
