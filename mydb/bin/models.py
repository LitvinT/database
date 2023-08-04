from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='name', blank=True)
    country = models.CharField(max_length=16, verbose_name='country', blank=True)
    email = models.EmailField(max_length=128, verbose_name='email', blank=True)
    phone = models.CharField(max_length=32, verbose_name='phone', blank=True, null=True, unique=True)
    login_bitmain = models.CharField(max_length=128, verbose_name='login_bitmain', blank=True)
    telegram_link = models.CharField(max_length=128, verbose_name='telegram_link', blank=True)
    instagram_link = models.CharField(max_length=128, verbose_name='instagram_link', blank=True)
    twitter_link = models.CharField(max_length=128, verbose_name='twitter_link', blank=True)
    vk_link = models.CharField(max_length=128, verbose_name='vk_link', blank=True)
    facebook_link = models.CharField(max_length=128, verbose_name='facebook_link', blank=True)
    linkedin_link = models.CharField(max_length=128, verbose_name='linkedin_link', blank=True)
    whatsapp_link = models.CharField(max_length=64, verbose_name='whatsapp_link', blank=True)
    counter = models.CharField(max_length=3, verbose_name='counter', blank=True)
    feedback = models.CharField(max_length=1024, verbose_name='feedback', blank=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='manager', blank=True, null=True)

    class Meta:
        db_table = 'clients'
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return self.name


class UpdateLog(models.Model):
    update_info = models.CharField(max_length=255)
    changes_before_update = models.JSONField(default=list)
    changes_after_update = models.JSONField(default=list)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.update_info


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, verbose_name='name', blank=True)
    country = models.CharField(max_length=16, verbose_name='country', blank=True)
    email = models.EmailField(max_length=128, verbose_name='email', blank=True)
    phone = models.CharField(max_length=32, verbose_name='phone', blank=True, null=True, unique=True)
    individual = models.CharField(max_length=64, verbose_name='first individual', blank=True)
    individual2 = models.CharField(max_length=64, verbose_name='second individual', blank=True)
    telegram_link = models.CharField(max_length=128, verbose_name='telegram_link', blank=True)
    instagram_link = models.CharField(max_length=128, verbose_name='instagram_link', blank=True)
    twitter_link = models.CharField(max_length=128, verbose_name='twitter_link', blank=True)
    vk_link = models.CharField(max_length=128, verbose_name='vk_link', blank=True)
    facebook_link = models.CharField(max_length=128, verbose_name='facebook_link', blank=True)
    linkedin_link = models.CharField(max_length=128, verbose_name='linkedin_link', blank=True)
    whatsapp_link = models.CharField(max_length=64, verbose_name='whatsapp_link', blank=True)
    counter = models.CharField(max_length=3, verbose_name='counter', blank=True)
    feedback = models.CharField(max_length=1024, verbose_name='feedback', blank=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='manager', blank=True, null=True)

    class Meta:
        db_table = 'company'
        verbose_name = 'сompany'
        verbose_name_plural = 'companies'

