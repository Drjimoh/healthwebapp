# Generated by Django 2.2 on 2020-02-24 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehealth', '0003_biodata_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodata',
            name='date_of_birth',
            field=models.DateTimeField(blank=True, default='2001-03-30'),
        ),
    ]
