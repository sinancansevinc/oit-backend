# Generated by Django 4.2.3 on 2023-08-21 09:23

import core.managers
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parent', models.ForeignKey(blank=True, limit_choices_to=models.Q(('parent__isnull', True), ('parent__parent__isnull', True), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='core.department')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(blank=True, max_length=150, null=True)),
                ('docplanner_id', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('last_name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(1)])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('country', models.CharField(blank=True, choices=[('pl', 'Poland'), ('de', 'Germany'), ('es', 'Spain'), ('it', 'Italy'), ('br', 'Brazil'), ('mx', 'Mexico'), ('tr', 'Turkey'), ('co', 'Colombia')], max_length=15, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('termination_date', models.DateTimeField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'permissions': (('can_access_all_users', 'can access all users'),),
            },
            managers=[
                ('objects', core.managers.UserManager()),
            ],
        ),
        migrations.AddIndex(
            model_name='department',
            index=models.Index(fields=['name'], name='core_depart_name_80d4fe_idx'),
        ),
        migrations.AddConstraint(
            model_name='department',
            constraint=models.UniqueConstraint(fields=('name',), name='unique_department_name'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['first_name', 'last_name'], name='core_user_first_n_7ed624_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['email'], name='core_user_email_38052c_idx'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['is_active'], name='core_user_is_acti_8c954f_idx'),
        ),
    ]
