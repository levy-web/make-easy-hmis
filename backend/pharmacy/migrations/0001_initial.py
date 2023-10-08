# Generated by Django 4.2.5 on 2023-10-06 18:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('max_daily_dose', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_daily_dose', models.DecimalField(decimal_places=2, max_digits=10)),
                ('strength', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], max_length=10)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('expiration_date', models.DateField()),
                ('created_by', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('item_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.item')),
            ],
        ),
    ]
