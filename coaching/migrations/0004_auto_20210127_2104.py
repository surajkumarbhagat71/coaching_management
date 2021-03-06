# Generated by Django 2.2.7 on 2021-01-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaching', '0003_studentcourse_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentpayment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='studentpayment',
            name='date_time',
        ),
        migrations.RemoveField(
            model_name='studentpayment',
            name='request_status',
        ),
        migrations.AddField(
            model_name='studentpayment',
            name='pay_amount',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentpayment',
            name='pay_date',
            field=models.DateTimeField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentpayment',
            name='pay_due',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentpayment',
            name='status',
            field=models.CharField(choices=[('0', 'Not paid'), ('1', 'pending'), ('2', 'paid')], max_length=200),
        ),
    ]
