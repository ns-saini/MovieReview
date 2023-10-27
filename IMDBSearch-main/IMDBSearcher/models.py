# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import django
from django.db import models
from django.utils import timezone


class Basic(models.Model):
    title_id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    create_timestamp = models.DateTimeField(default=django.utils.timezone.now)
    update_timestamp = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # managed = False
        app_label = 'IMDBSearcher'
        db_table = 'basic'


class Names(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(null=True)
    death_year = models.IntegerField(blank=True, null=True)
    primary_profession = models.CharField(max_length=250, blank=True, null=True)
    create_timestamp = models.DateTimeField(default=django.utils.timezone.now)
    update_timestamp = models.DateTimeField(default=django.utils.timezone.now, blank=True, null=True)

    class Meta:
        # managed = False
        app_label = 'IMDBSearcher'
        db_table = 'names'


class Principal(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.ForeignKey(Names, models.DO_NOTHING)
    category = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=40, blank=True, null=True)
    characters = models.CharField(max_length=100, blank=True, null=True)
    create_timestamp = models.DateTimeField(default=django.utils.timezone.now)
    update_timestamp = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # managed = False
        app_label = 'IMDBSearcher'
        db_table = 'principal'


class Ratings(models.Model):
    title_id = models.CharField(primary_key=True, max_length=100)
    avg_rating = models.DecimalField(max_digits=10, decimal_places=1)
    votes = models.IntegerField()
    create_timestamp = models.DateTimeField(default=django.utils.timezone.now)
    update_timestamp = models.DateTimeField(default=django.utils.timezone.now)

    class Meta:
        # managed = False
        app_label = 'IMDBSearcher'
        db_table = 'ratings'


class TitleToName(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.OneToOneField(Names, models.DO_NOTHING)
    title = models.OneToOneField(Basic, models.DO_NOTHING)

    class Meta:
        # managed = False
        app_label = 'IMDBSearcher'
        db_table = 'title_to_name'
