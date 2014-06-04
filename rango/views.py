# coding=utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from time import time, localtime


def _process_request(request, context_dict=None, fn=None):
    """
    :param request:
    :param context_dict: optional dictionary passed to func:render_to_response
    :param fn: html file from templates
    :return: HttpResponse Object
    """
    # Request the context of the request
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Return the rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note the the first parameter is the template we wish to use.
    return render_to_response(fn, context_dict, context)


def index(request):
    """
    :param request:
    :return:
    """
    # Construct a dictionary to pass to the template engine as it's context
    # Note the key boldmessage is the same as {{ boldmessage }} in the template: rango/index.html
    context_dict = {"boldmessage": "I am bold font from the context"}
    return _process_request(request, context_dict, r"rango/index.html")


def about(request):
    """
    :param request:
    :return:
    """
    # Construct a dictionary to pass to the template engine as it's context
    # Note the value from key timestamp is an instance of GetLocalTime, and "now" is an attribute of that class
    # {{ timestamp.now }} in the template: rango/about.html returns the localtime
    context_dict = {"timestamp": GetLocalTime()}
    return _process_request(request, context_dict, r"rango/about.html")


class SilentAssertionError(Exception):
    silent_variable_failure = True


class GetLocalTime(object):
    def now(self):
        try:
            t = localtime(time())
            return( '%04d-%02d-%02d %02d:%02d:%02d'%(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec) )
        except SilentAssertionError:
            return "ooops"