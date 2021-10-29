# Generated by Django 2.2.24 on 2021-09-05 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Spaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='başlık')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='açıklama')),
                ('slug', models.SlugField(editable=False, max_length=130, unique=True)),
                ('profile_pic', models.ImageField(blank=True, default='default.jpg', upload_to='space_pictures', verbose_name='profilepic')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='space', to=settings.AUTH_USER_MODEL, verbose_name='kurucu')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
