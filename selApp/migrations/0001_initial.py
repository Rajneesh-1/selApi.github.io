# Generated by Django 3.2 on 2022-07-12 05:15

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import selApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AvailableCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availableCity', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100)),
                ('description', models.CharField(default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='pictures')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.CharField(max_length=1000000)),
                ('message_date', models.CharField(default=0, max_length=1000)),
                ('user', models.CharField(max_length=1000000)),
                ('belongs_to_room', models.CharField(max_length=1000000)),
            ],
        ),
        migrations.CreateModel(
            name='MobileRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobileNo', models.CharField(max_length=10)),
                ('otptimeStamp', models.CharField(max_length=100)),
                ('otp', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PersonInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('occupation', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
                ('imageUrl', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Pin_Unpin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin_id', models.IntegerField()),
                ('pin_ka_id', models.CharField(max_length=1000)),
                ('pin_permission', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='seen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('users_ka_name', models.CharField(max_length=10000)),
                ('special_id', models.CharField(max_length=10000)),
                ('roomnm', models.CharField(default=0, max_length=10000)),
                ('time_of_reject', models.CharField(default=0, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TotalCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalCity', models.CharField(max_length=1000000)),
            ],
        ),
        migrations.CreateModel(
            name='user_involved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Room_ka_name', models.CharField(max_length=1000)),
                ('user_ka_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='waiting_users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_room', models.CharField(max_length=1000)),
                ('users_message', models.CharField(max_length=1000)),
                ('users_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('user_inv', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='selApp.myuser')),
                ('Room_name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Selectoptions',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='selApp.myuser')),
                ('city_name', models.CharField(max_length=70)),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('unique_key', models.CharField(default=0, max_length=100, validators=[selApp.models.Selectoptions.validate_ukey])),
                ('incr', models.CharField(default=1, max_length=1)),
                ('date_time', models.CharField(default=1, max_length=30)),
                ('combKey', models.CharField(default=1, max_length=5)),
                ('time_check', models.CharField(default=1, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='weather_ackno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messages', models.CharField(default=1, max_length=10000)),
                ('time_of_message', models.CharField(default=0, max_length=1000)),
                ('messages_alert', models.CharField(default=0, max_length=1)),
                ('weatherType', models.CharField(default=0, max_length=20)),
                ('maxTemp', models.CharField(default=0, max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration')),
            ],
        ),
        migrations.CreateModel(
            name='UserAdditionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fcmToken', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=100)),
                ('date', models.CharField(max_length=100)),
                ('scheduleItem', models.CharField(max_length=1000)),
                ('pinned', models.CharField(default=0, max_length=1)),
                ('lastScheduleOn', models.CharField(default='12-07-2022', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='selApp.mobileregistration')),
            ],
        ),
        migrations.CreateModel(
            name='Scheduled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_items', models.TextField()),
                ('schedule_date', models.DateField(validators=[selApp.models.Scheduled.validate_date])),
                ('schedule_time', models.TimeField(validators=[selApp.models.Scheduled.validate_time])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpiredItemList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expired_time', models.CharField(max_length=100)),
                ('expired_date', models.CharField(max_length=100)),
                ('scheduleItem', models.CharField(max_length=1000)),
                ('pinned', models.CharField(default=0, max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration')),
            ],
        ),
        migrations.CreateModel(
            name='expired_scheduledList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_items', models.TextField()),
                ('schedule_date', models.DateField()),
                ('schedule_time', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('town', models.CharField(max_length=40)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration')),
            ],
        ),
        migrations.CreateModel(
            name='capture_schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capture_schedule_time', models.CharField(max_length=100)),
                ('cap_sch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40, verbose_name='Key')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration')),
            ],
        ),
        migrations.AddField(
            model_name='myuser',
            name='userMobileLinked',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='selApp.mobileregistration'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Grp_admin',
            fields=[
                ('related_room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='selApp.room')),
                ('G_a', models.CharField(max_length=1000)),
                ('preference', models.CharField(max_length=10)),
                ('he_is_adm_of', models.CharField(max_length=1000)),
            ],
        ),
    ]
