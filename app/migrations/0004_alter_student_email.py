# Generated by Django 4.0.6 on 2023-07-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_student_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=128, primary_key=True, serialize=False),
        ),
    ]
