# coding=utf-8
"""
Create models here.  To verify, use manage.py
./manage.py sql rango
"""
from django.db import models
import re

# Create your models here.
class Category(models.Model):
    """
    Model class, contains attributes:
        name, views, likes
    """
    name = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # encode/decode translaters
    _url_encode_rules_dict = {
        " ": "_",
        "#": "&#35;",
        "%": "&#37",
        r"\\": "&#92",
        }

    def __init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        # encode a_name to a url valid name, mainly for handling unsafe characters such as spaces, tabs,
        # chevrons, hash-tag, tilde, pipe, backslash, carrot, curly braces, square brackets, etc,
        self.url = self._encode_url_name(self.name, self._url_encode_rules_dict)

    def _encode_url_name(self, a_str, rules_dict):
        new_str = a_str
        for grep_regex, sub_regex in rules_dict.iteritems():
            new_str = re.sub(grep_regex, sub_regex, new_str)
        return new_str

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