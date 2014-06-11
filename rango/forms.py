# coding=utf-8
"""
Module for forms used with Page and Category Models, based on Django's ModelForm
"""
__author__ = "jk"


from django import forms
from rango.models import Category, Page
import re


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    url = forms.CharField(max_length=200, widget= forms.HiddenInput, initial="name_url", required=False)
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between ModelForm and model
        model = Category
        fields = ["name"]


class PageForm(forms.ModelForm):
    """
    PageForm for adding a page model instance to a category model object
    """
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean(self):
        """
        If url is not empty and doesn't start with "http:/", prepend http://
        :return:
        """
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        if url and not re.search("^http://", url):
            cleaned_data["url"] = "http://{0}".format(url)
        return cleaned_data

    class Meta:
        """
        Special handling instructions for attributes not handled by Model
        """
        # Provide an association between the ModelForm and the model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here we are hiding the foreign key.
        fields = ("title", "url", "views")