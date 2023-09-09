# Generated by Django 4.1.7 on 2023-07-16 13:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartChapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.chapter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='chapter',
            name='cart',
            field=models.ManyToManyField(through='novels.CartChapter', to=settings.AUTH_USER_MODEL),
        ),
    ]
