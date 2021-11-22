from django.db import migrations, models
import django.db.models.deletion
import nautobot.ipam.fields
import nautobot_ddns.validators
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('server', models.CharField(max_length=255, validators=[nautobot_ddns.validators.HostnameAddressValidator()])),
                ('tsig_key_name', models.CharField(max_length=255, validators=[nautobot_ddns.validators.HostnameValidator()])),
                ('tsig_algorithm', models.CharField(max_length=32)),
                ('tsig_key', models.CharField(max_length=512, validators=[nautobot_ddns.validators.validate_base64])),
            ],
            options={
                'verbose_name': 'dynamic DNS Server',
                'verbose_name_plural': 'dynamic DNS Servers',
                'ordering': ('server', 'tsig_key_name'),
                'unique_together': {('server', 'tsig_key_name')},
            },
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True, validators=[nautobot_ddns.validators.HostnameValidator()])),
                ('ttl', models.PositiveIntegerField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nautobot_ddns.server')),
            ],
            options={
                'verbose_name': 'forward zone',
                'verbose_name_plural': 'forward zones',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ReverseZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('prefix', nautobot.ipam.fields.VarbinaryIPField(unique=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('ttl', models.PositiveIntegerField()),
                ('server', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nautobot_ddns.server')),
            ],
            options={
                'verbose_name': 'reverse zone',
                'verbose_name_plural': 'reverse zones',
                'ordering': ('prefix',),
            },
        ),
    ]