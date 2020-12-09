Installation
============

The ``polls`` module has been packaged into a python library installable via ``pip``.

.. code:: bash

    pip install django-polls

Requirements
--------------

This tutorial was developed using 
`Python 3.9 <https://docs.python.org/3/whatsnew/3.9.html>`_

The following table is a list of packages and versions used throughout the 
various sections of development explored in this tutorial. All of these packages 
were installed with ``pip``. An |RST| Simple Table was used to document this 
requirements table which was derived from a `> pip list` 

==================    =======  ===============
Package               Version  Related Section
==================    =======  ===============
Django                3.1.3
django-extensions     3.0.9    
Pillow                7.2.0    Image I/O
reportlab             3.5.55   PDF Generation
setuptools            49.1.3   Packaging
Sphinx                3.3.1    Documentation
sphinx-rtd-theme      0.5.0    Documentation
virtualenv            20.0.30  Configuration
xhtml2pdf             0.2.5    PDF Generation
==================    =======  ===============

.. TODO:: provide example shell trace

Development environment
---------------------------

#. If you don't have it, install ``pip``, the python package installer
#. We recommend using ``virtualenv`` for development. It is great to have 
   a separate environment for each project, keeping the dependencies 
   for multiple projects separated
#. Create a virtualenv for the project. This can be inside the project
   directory, but cannot be under version control
#. Activate your virtualenv by sourcing the virtualenv script
#. Goto the project directory and run
    .. code:: bash

        ./manage.py runserver

#. when done deactivate the virtualenv via 

    .. code:: bash

        deactivate


.. |RST| replace:: reStructuredText
