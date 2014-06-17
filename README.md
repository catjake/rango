rango
=====

walk through tutorial from www.tangowithdjango.com

Overview:

    Tutorial for django and developer tools such as git

Git Cheatsheet:

    * git pull  # sync remote repository with local copy
    * git commit <file_name> # committing changes to local repository
    * git push origin master # committing changes to remote repository

Design Brief:

    For the main page of the site, they would like visitors to be able to see:

    * the 5 most viewed pages;
    * the five most rango’ed categories; and
    * some way for visitors to browse or search through categories.
    * When a user views a category page, they would like it to display:
        ** the category name, the number of visits, the number of likes;
        ** along with the list of associated pages in that category 
           (showing the page’s title and linking to its url); and.
        ** some search functionality (via Bing’s Search API) to find other 
           pages that can be linked to this category.

    For a particular category, the client would like the name of the category 
    to be recorded, the number of times each category page has been visited, 
    and how many users have clicked a “like” button (i.e. the page gets rango’ed, 
    and voted up the social hierarchy).

    Each category should be accessible via a readable URL - for example, 
    /rango/books-about-django/.

    Only registered users will be able to search and add pages to categories. 
    And so, visitors to the site should be able to register for an account.

Cheatsheet:

    Create a new Django Project:
    * django-admin startproject <projname> <dest>
    Create a new Django Application:
    # python manage.py startapp <appname>
    # Add appname to settings.INSTALLED_APPS tuple
    # In projname urls.py file, add a mapping to the application (appname)
    # In appname directory create urls.py file to direct incoming URL strings to views
    # In appname view.py, create required views ensuring that they return a HttpResponse object


Status:

+ Chapters 1-7:
    * Added templates for index and about in views
    * Added functionality for displaying images in static files location, designated by STATICFILES_DIR
    * Added media server
    * Created and synced sqlite3 database
    * Registered models to admin interface
    * Developed population script
    * Sourced data from models to views
    * Added (views) details page to templates for each Category.name and corresponding Page objects
    * Created Page and Category Forms
    * Added views for creating new category and adding a page to an existing category
+ Chapter 8:
    * Setup Authentication
    * Added user attributes
    * Created UserRegistration View, Template, and Form
    * Added Login Functionality
    * Created Login View and Template
    * Added logout functionality
    * Set user permissions for adding or modifying categories and pages based on user.is_authenticated()
+ Chapter 9:
    * Implemented template for html layout