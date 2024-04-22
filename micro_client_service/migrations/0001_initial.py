# Generated by Django 4.1.7 on 2023-06-21 04:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('micro_auth_service', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilingDetails',
            fields=[
                ('pan', models.CharField(default='', max_length=10, primary_key=True, serialize=False)),
                ('itr_plan', models.CharField(blank=True, max_length=50, null=True)),
                ('form_submit_date', models.CharField(blank=True, max_length=20, null=True)),
                ('filing_date', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FootPrints',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('footprint', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('date', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceDetails',
            fields=[
                ('invoice_number', models.CharField(default='', max_length=50, primary_key=True, serialize=False)),
                ('invoice_date', models.CharField(blank=True, max_length=20, null=True)),
                ('invoice_filename', models.CharField(blank=True, max_length=30, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_details', to='micro_auth_service.clientcredentials')),
            ],
        ),
        migrations.AddIndex(
            model_name='footprints',
            index=models.Index(fields=['date'], name='micro_clien_date_4b4e5a_idx'),
        ),
        migrations.AddField(
            model_name='filingdetails',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='micro_auth_service.clientcredentials'),
        ),
    ]