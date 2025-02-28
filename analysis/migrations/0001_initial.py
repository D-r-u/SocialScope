# Generated by Django 5.1.5 on 2025-02-28 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0003_delete_sentimentanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentimentAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_file', models.FileField(blank=True, null=True, upload_to='sentiment_csvs/')),
                ('keywords', models.JSONField(default=list)),
                ('result', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyses', to='inventory.productsinventory')),
            ],
        ),
    ]
