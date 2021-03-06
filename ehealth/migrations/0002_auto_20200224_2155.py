# Generated by Django 2.2 on 2020-02-24 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehealth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biodata',
            name='age',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='biodata',
            name='blood_glucose_level',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='biodata',
            name='bmi',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='biodata',
            name='weight_unit',
            field=models.CharField(blank=True, choices=[('kg', 'kilograme'), ('Ibs', 'Pounds')], max_length=250, null=True),
        ),
    ]
