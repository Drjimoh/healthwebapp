# Generated by Django 2.2 on 2020-02-24 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehealth', '0002_auto_20200224_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='biodata',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, default='2001-03-30'),
        ),
    ]
