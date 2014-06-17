# coding=utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from time import time, localtime
from models import Category, Page
from forms import CategoryForm, PageForm, UserForm, UserProfileForm


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
    Query the database for a list of ALL categories currently stored
    Order the categories by "likes" in descending order
    Retrieve the top 5 only - or all if less than 5
    Place the list in dictionary:context_dict and pass to the template engine: index.html
    :param request:
    :return:
    """
    # GET category list, sort by "likes" in descending order -> order_by("-likes")
    # For each category object returned, add attribute "url", replace " " with "_"
    category_list = Category.objects.order_by("-likes")[:5]
    for a_category in category_list[:5]:
        if not hasattr(category,"url"):
            setattr(a_category,"url", Category._encode_url_name(a_category.name))

    # GET page list, sort descending by "views", just the top 5
    page_list = Page.objects.order_by("-views")[:5]

    # Construct a dictionary to pass to the template engine as it's context
    # Note the key boldmessage is the same as {{ boldmessage }} in the template: rango/index.html
    context_dict = {
        "boldmessage": "You are welcome to register or login",
        "categories": category_list,
        "pages": page_list,
    }
    return _process_request(request, context_dict, r"rango/index.html")


def all_categories(request):
    """
    View for all categories, with option to add a category if user logged in
    :param request:
    :return:
    """
    # GET category list, sort by "likes" in descending order -> order_by("-likes")
    # For each category object returned, add attribute "url", replace " " with "_"
    category_list = Category.objects.order_by("-likes")
    context_dict = {
        "categories": category_list,
        }
    return _process_request(request, context_dict, r"rango/all_categories.html")


def category(request, category_name_url):
    """
    Generate details page base on request and category_name_url
    This involves the url design and mapping workflow step by
    obtaining (GET) the context of the request, populate the context_dict with the
    category and page data, render the template, and send the result back (POST)
    :param request:
    :param category_name_url:
    :return:
    """
    # Change underscores in the category name to spaces
    # URLs don't handle spaces well, so encode them as underscores
    # Just replacing the underscores with spaces again to get Category.name
    pages = []
    a_category = None
    category_name = "oops"
    try:
        # Find category_name using method:get()
        # Which returns one model instance or raises Exception:DoesNotExist
        # a_category = Category.objects.get(name=category_name)
        a_category = Category.objects.get(url=category_name_url)
        category_name = a_category.name
        # Retrieve all association pages to category_name
        # Note: filter returns >= 1 model instance(s)
        pages = Page.objects.filter(category=a_category)  # linked by model.ForeignKey(Category) attribute
    except Category.DoesNotExist:
        # Specified category name was not found
        # Handle Exception in template with if - else conditional by displaying "no category"
        pass
    # Add results list and category object from database to context_dict
    # Verification that the category exists is handled in the template:category.html
    context_dict = {
        "category_name": category_name,
        "pages": pages,
        "category": a_category,
        }
    return _process_request(request, context_dict, r"rango/category.html")


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


def add_category(request):
    """
    Either show a form or create a new instance of one.
    """

    # Is request HTTP POST or GET?
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            setattr(category,"url", Category._encode_url_name(category.name))
            category.save()

            # now call the index() view
            # user redirected to home page
            return index(request)
        else:
            # Uh oh, supplied form contains error - print out to console
            print form.errors
    else:
        # request not a POST, display the form to enter details
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return _process_request(request, {"form": form}, "rango/add_category.html")


def add_page(request, category_name_url):
    """
    Add page to category if it doesn't exist,
    :param request
    :param category_name_url
    """
    category_name = Category._encode_url_name(category_name_url, Category._url_decode_rules_dict)
    # category_name = "ooops"
    cat = None
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            # Cannot commit straight away, not all fields automatically populated
            page = form.save(commit=False)

            # Retrieve the associated Category object so we can add it
            # Handle exception for Model.DoesNotExist, Go back and render the add category form
            try:
                cat = Category.objects.get(url=category_name_url)
                page.category = cat
            except Category.DoesNotExist:
                # Category does not exist, Go back and the render the add_category form
                return _process_request(request, {}, "rango/add_category.html")
            # set default value for number of views, and save new model instance
            page.views = 0
            page.save()

            # Now that the page is saved, display the category instead.
            return category(request, category_name_url)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {
        "category_name_url": category_name_url,
        "category_name": category_name,
        "form": form,
    }
    return _process_request(request, context_dict, "rango/add_page.html")


def register(request):
    """
    View for register new User
    """
    # Boolean value: True-> registration succeeded, initially set to False
    registered = False

    #If it's a HTTP POST, process the form data:
    if request.method == "POST":
        # Making use of both UserForm and UserProfileForm to grab information
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid....
        if user_form.is_valid() and profile_form.is_valid():
            # Save user's form data to database
            user = user_form.save()

            # Now hash the password and update the user object
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance, Set commit=False so
            # user attributes like picture, website, etc. can be set
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user enter a profile picture?
            # If so, get from the input form and put it in the UserProfile Model
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            # Now UserProfile model instance can be saved
            profile.save()
            registered = True  # used to determine that template registration was successful.
        # Uh oh, invalid form or forms?  Print out problems to the terminal, also shown to user
        else:
            print user_form.errors, profile_form.errors
    else:
        # Not a HTTP POST, so form rendered with two fresh blank ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render the template depending on the context
    context_dict = {
        "user_form": user_form, "profile_form": profile_form, "registered": registered
    }
    return _process_request(request, context_dict, "rango/register.html")


def user_login(request):
    """
    User login view
    """
    # if request is HTTP POST, try to pull out the relevant info
    if request.method == "POST":
        # Gather user name and password entries from the login form.
        username = request.POST["username"]
        password = request.POST["password"]

        # Use django's builtin's to see if the username/password combination is valid
        # User object returned if so
        user = authenticate(username=username, password=password)

        # user is a User object instance, then details are correct
        # else no matching credentials found
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/rango/")
            else:  # account inactive, no login for you!
                return HttpResponse("Sorry for the inconvenience, your account is disabled.")
        else:  # Bad login details provided, No user credentials found
            error_msg = "<p style=\"margin-left:10px;\">One or both are invalid login details: " \
                        "<br/>    user: {0}, password: {1}<br/>".format(username, password)
            error_msg = "Ooops, invalid login details supplied.<br/>{0}<br/>" \
                        "<a href=\"/rango/login/\">Try Again?<a/><br/><a href=\"/rango\">Or just browse...<a/>" \
                        "<p/>".format(error_msg)
            return HttpResponse(error_msg)
    else:
        # The request is not a HTTP POST, so display login form and go from there
        # No context variables to pass to the template system, hence the blank dictionary
        # object, context_dict
        context_dict = {}
        return _process_request(request, context_dict, "rango/login.html")


@login_required
def restricted(request):
    """
    Used with decorator django.contrib.auth.decorators.login_required, to restrict access to only
    those logged in.  For user's not logged in, redirect to /rango/login/
    """
    context_dict = {
        "message": "Since you're logged in, you can see this!",
    }
    return _process_request(request, context_dict, "rango/restricted.html")


@login_required
def user_logout(request):
    """
    Used with login_required decorator, we know user is logged in, now just log them out
    and redirect to rango home page
    Note: In this simple view, we don't need RequestContext()
    """
    logout(request)
    return HttpResponseRedirect("/rango/")


class SilentAssertionError(Exception):
    silent_variable_failure = True


class GetLocalTime(object):
    def now(self):
        try:
            t = localtime(time())
            return'%04d-%02d-%02d %02d:%02d:%02d'%(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        except SilentAssertionError:
            return "ooops"