from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='bookings.booking'),
        ),
    ]


