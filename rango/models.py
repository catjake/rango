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
    url = models.CharField(max_length=200, unique=False)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    # encode/decode translator, not exhaustive, just enough for book exercises
    _url_encode_rules_dict = {
        " ": "_",
        "#": "&#35;",
        "%": "&#37",
        r"\\": "&#92",
    }
    _url_decode_rules_dict = {v:k for k, v in _url_encode_rules_dict.iteritems()}

    def __del__init__(self, *args, **kwargs):
        super(Category, self).__init__(*args, **kwargs)
        self.url = self._encode_url_name(self.name, self._url_encode_rules_dict)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    @staticmethod
    def _encode_url_name(a_str, rules_dict=_url_encode_rules_dict):
        """
        encode a_name to a url valid name, mainly for handling unsafe characters such as spaces, tabs,
        chevrons, hash-tag, tilde, pipe, backslash, carrot, curly braces, square brackets, etc,
        :param a_str
        :param rules_dict
        :return valid url name encoded from a_str
        """
        new_str = a_str
        for grep_regex, sub_regex in rules_dict.iteritems():
            new_str = re.sub(grep_regex, sub_regex, new_str)
        return new_str



class Page(models.Model):
    """
    Model class, contains attributes:
        category, title, url, and views
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField(max_length=200)
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title