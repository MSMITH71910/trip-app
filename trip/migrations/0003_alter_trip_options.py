# Generated by Django 5.1.7 on 2025-04-02 01:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0002_remove_budgetitem_date_remove_itineraryitem_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['-start_date']},
        ),
    ]
