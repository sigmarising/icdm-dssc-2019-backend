# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Article(models.Model):
    category = models.CharField(primary_key=True, max_length=255)
    identity = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    graphweak = models.TextField(db_column='graphWeak', blank=True, null=True)  # Field name made lowercase.
    graphmedium = models.TextField(db_column='graphMedium', blank=True, null=True)  # Field name made lowercase.
    graphstrong = models.TextField(db_column='graphStrong', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'article'
        unique_together = (('category', 'identity'),)
