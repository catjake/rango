# coding=utf-8
"""
Create models here.  To verify, use manage.py
./manage.py sql rango
"""
from django.db import models

# Create your models here.
class Category(models.Model):
    """
    Model class, contains attributes:
        name, views, likes
    """
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name


class Page(models.Model):
    """
    Model class, contains attributes:
        category, title, url, and views
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title