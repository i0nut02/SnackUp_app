# Generated by Django 4.0.6 on 2023-07-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_student_name_remove_student_surname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
    ]
