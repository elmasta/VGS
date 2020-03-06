# Generated by Django 3.0.3 on 2020-03-06 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20200306_0223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='compilation',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='games',
            options={'ordering': ('name',)},
        ),
        migrations.RemoveField(
            model_name='games',
            name='compilation',
        ),
        migrations.AddField(
            model_name='games',
            name='compilation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='collection.Compilation'),
        ),
    ]
