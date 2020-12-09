.. Django Polls documentation master file, created by
   sphinx-quickstart on Mon Dec  7 10:21:37 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Polls's documentation!
========================================

This is a good place for *some* kind of **introduction** or overview.

.. note:: This tutorial was largely based on the Django_ Tutorial Documentation.

.. topic:: Your Topic Title

     Subsequent indented lines comprise
         the body of the topic, and are
             interpreted as body elements.

.. warning:: note the space between the directive and the text

.. image:: ../../../static/img/me.jpg
   :width: 200
   :alt: Splash Image

.. sidebar:: Sidebar Title
    :subtitle: Optional Sidebar Subtitle

    Subsequent indented lines comprise
    the body of the sidebar, and are
    interpreted as body elements.

Adding the ``sphinx.ext.todo`` extension will allow us to maintain an overall
todo list here which accumilates the todo directives throughout the documentation.
It requires ``todo_include_todos=True`` in the ``conf.py``

.. todolist::

.. toctree::
   :maxdepth: 3                    
   :caption: Contents:

   usage
   install
   modules/views.rst
   modules/models.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _Django: https://docs.djangoproject.com/en/3.1/

