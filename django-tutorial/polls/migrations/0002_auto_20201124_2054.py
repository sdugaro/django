# Generated by Django 3.1.3 on 2020-11-24 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_img',
            field=models.ImageField(default='', null=True, upload_to='pdf'),
        ),
        migrations.AddField(
            model_name='question',
            name='question_pdf',
            field=models.FileField(default='', null=True, upload_to='img'),
        ),
    ]