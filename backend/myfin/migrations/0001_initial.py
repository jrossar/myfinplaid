# Generated by Django 4.0.2 on 2022-05-22 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=320, unique=True, verbose_name='Email')),
                ('user_name', models.CharField(max_length=150, unique=True, verbose_name='User Name')),
                ('first_name', models.CharField(max_length=20, verbose_name='First Name')),
                ('password', models.CharField(max_length=30, verbose_name='Password')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_staff', models.BooleanField(verbose_name='Is Staff')),
                ('is_superuser', models.BooleanField(verbose_name='Is Superuser')),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MyFin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('secret_key', models.CharField(max_length=24)),
                ('client_id', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=42, verbose_name='Transaction ID')),
                ('category', models.CharField(max_length=30, verbose_name='Transaction ID')),
                ('name', models.CharField(max_length=40, verbose_name='Name')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Amount')),
                ('pending', models.BooleanField(verbose_name='Pending')),
                ('iso_currency_code', models.CharField(max_length=10, verbose_name='Currency')),
                ('account_id', models.CharField(max_length=40, verbose_name='Account ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of Transaction')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
