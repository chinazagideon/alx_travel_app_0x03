from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_add_payment_booking_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.booking'),
        ),
    ]


