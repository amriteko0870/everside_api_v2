# Generated by Django 4.0.3 on 2022-05-12 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='everside_nps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_id', models.CharField(max_length=100)),
                ('review', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('polarity_score', models.CharField(max_length=100)),
                ('nps_score', models.CharField(max_length=100)),
                ('nps_label', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('clinic', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('timestamp', models.BigIntegerField()),
            ],
        ),
    ]
