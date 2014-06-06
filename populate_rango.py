#!/usr/bin/env python
# coding=utf-8
import os


def populate():
    """
    Population script for rango.db, add members for Category and Page models
    :return:
    """
    pages_dict = {
        "Python": {
            "cat_args": {"likes": 64, "views": 128},
            "pargs_list":
                [
                    {"title": "Official Python Tutorial",
                     "url": "http://docs.python.org/2/tutorial/", },
                    {"title": "How to Think like a Computer Scientist",
                     "url": "http://www.greenteapress.com/thinkpython/",},
                    {"title": "Learn Python in 10 Minutes",
                     "url": "http://www.korokithakis.net/tutorials/python/",},
                ],
        },
        "Django": {
            "cat_args": {"likes": 32, "views": 64},
            "pargs_list":
                [
                    {"title": "Official Django Tutorial",
                     "url": "https://docs/djangoproject.com/en/1.5/intro/tutorial01/",},
                    {"title": "Django Rocks",
                     "url": "http://www.djangorocks.com/",},
                    {"title": "How to Tango with Django",
                     "url": "http://www.tangowithdjango.com/",},
                ],
        },
        "Other Frameworks": {
            "cat_args": {"likes": 16, "views": 32},
            "pargs_list":
                [
                    {"title": "Bottle",
                     "url": "http://bottlepy.org/docs/dev/",},
                    {"title": "Flask",
                     "url": "http://flask.pocoo.org",},
                ],
        },
    }
    for cat_name, a_dict in pages_dict.iteritems():
        a_cat, is_created = add_to_model(Category, name=cat_name, **a_dict["cat_args"])
        for kwargs in a_dict["pargs_list"]:
            a_page, is_created = add_to_model(Page, category=a_cat, **kwargs)
            print " - {0} - {1}".format(str(a_cat), str(a_page))


def add_to_model(model, **model_kwargs):
    """
    Add a member object to Model class
    :param model: django.db.models.Model object
    :return: Model object member, boolean created (was created->True or was not created->False)
    """
    m, created = model.objects.get_or_create(**model_kwargs)
    return m, created


if __name__ == "__main__":
    print "Starting Rango population script...."
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")
    from rango.models import Category, Page
    populate()
