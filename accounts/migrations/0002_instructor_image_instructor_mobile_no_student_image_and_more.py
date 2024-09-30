# Generated by Django 5.0.6 on 2024-07-09 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='image',
            field=models.ImageField(default='exit', upload_to='patient/images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructor',
            name='mobile_no',
            field=models.CharField(default='exit', max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.ImageField(default='exit', upload_to='patient/images/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='mobile_no',
            field=models.CharField(default='exit', max_length=12),
            preserve_default=False,
        ),
    ]
