# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DigestAuthCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_nonce', models.TextField()),
                ('client_nonce', models.TextField()),
                ('client_counter', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='digestauthcounter',
            unique_together={('server_nonce', 'client_nonce')},
        ),
    ]
