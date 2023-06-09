# Generated by Django 4.2.1 on 2023-05-30 07:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autoservisasinfo', '0002_remove_uzsakymas_order_number_delete_uzsakymoeilute'),
    ]

    operations = [
        migrations.CreateModel(
            name='UzsakymoEilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='count')),
                ('total_price', models.FloatField(verbose_name='total_price')),
                ('paslauga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzsakymoEilutes', to='autoservisasinfo.paslauga', verbose_name='paslaugos')),
                ('uzsakymas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uzsakymoEilutes', to='autoservisasinfo.uzsakymas', verbose_name='uzsakymai')),
            ],
            options={
                'verbose_name': 'uzsakymoEilute',
                'verbose_name_plural': 'uzsakymoEilutes',
            },
        ),
    ]
