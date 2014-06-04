# coding=utf-8
from django.http import HttpResponse


def index(request):
    """
    :param request:
    :return:
    """
    request = HttpResponse()
    request.write("<p>Rango says hello and happy New Year!</p>")
    request.write("<p>Links:<br>")
    request.write("<a href=/rango/about>    About</a></p>")
    return request


def about(request):
    """
    :param request:
    :return:
    """
    request = HttpResponse()
    request.write("<p>Rango says: Here is the about page</p>")
    request.write("<p><a href=/rango>Back to Main</a></p>")
    return request