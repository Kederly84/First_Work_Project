# Generated by Django 4.1.3 on 2022-11-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportapp', '0003_alter_reportdata_absenteeism_alter_reportdata_ready_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportdata',
            options={'ordering': ['date', 'contact_center', 'group', 'full_name', 'rating'], 'verbose_name': 'Данные отчета', 'verbose_name_plural': 'Данные отчета'},
        ),
        migrations.AddField(
            model_name='reportdata',
            name='rating',
            field=models.FloatField(default=0, verbose_name='Рейтинг'),
        ),
    ]