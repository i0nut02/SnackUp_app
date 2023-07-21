# Generated by Django 4.0.6 on 2023-07-14 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField()),
                ('section', models.CharField(max_length=1)),
                ('specialisation', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('surname', models.CharField(max_length=64)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.classroom')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=128)),
                ('street_number', models.PositiveIntegerField()),
                ('zip_code', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
            ],
            options={
                'unique_together': {('street', 'street_number', 'zip_code')},
            },
        ),
        migrations.AddField(
            model_name='classroom',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.school'),
        ),
        migrations.AlterUniqueTogether(
            name='classroom',
            unique_together={('school', 'grade', 'section', 'specialisation')},
        ),
    ]