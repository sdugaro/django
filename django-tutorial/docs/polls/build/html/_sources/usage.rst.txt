Usage
==========

Here is a python Code block
---------------------------

.. code:: python

   from django.core.paginator import Paginator 

   class BootstrapPaginator(Paginator):
    """
    A paginator that does not return the entire range, rather
    a few wing pages on either side of the current page.
    """
    def __init__(self, *args, **kwargs):
        """Initialize Paginator parameters, defaulting extended parameters

        Args:
            wing_pages (int): default 2
                the number of pages shown before and after the current page.
            max_pages (int): defaut 5
                the total number of pages to show in the pagination range
        """
        self.max_pages = kwargs.pop('max_pages', 5)
        self.wing_pages = kwargs.pop('wing_pages', 2)
        #super(BootstrapPaginator, self).__init__(*args, **kwargs)  # Py2k
        super().__init__(*args, **kwargs)  # Py3k

    def _get_page(self, *args, **kwargs):
        self.page = super(BootstrapPaginator, self)._get_page(*args, **kwargs)
        return self.page

    @property
    def page_range(self):
        fold_min = max(self.page.number - self.wing_pages, 1)
        fold_max = fold_min + self.max_pages
        logger.debug(f"fold_min[{fold_min}] fold_max[{fold_max}]")
        if fold_max > self.num_pages:
            fold_min = self.num_pages - self.max_pages + 1
            fold_max = self.num_pages + 1

        fold_range = range(fold_min, fold_max)
        logger.debug(f"fold_range={fold_range}")
        return fold_range


3rd Level Deep Title to show some DocText Blocks
````````````````````````````````````````````````

>>> class Calc:
...   def add(*args):
...     return sum(map(float,args))
...
>>> Calc.add(1,2,3,'4','5','6')
21.0
>>> c = Calc()
>>> c.add(1,2,3,'4','5','6')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in add
TypeError: float() argument must be a string or a number, not 'Calc'

>>> class Calc:
...   @staticmethod
...   def add(*args):
...     return sum(map(float,args))
...
>>> c = Calc()
>>> Calc.add(1,2,3,'4','5','6')
21.0
>>>




Here is some css and html used for keyframe animation
-----------------------------------------------------

.. code:: css

    #terrain {
        width: 600px;
        height: 600px;
        margin: 2% auto;
        background: url("images/spritesheet_bg.png");
        animation: play_terrain 4s steps(68) infinite;
    }

    @keyframes play_terrain {
        100% { background-position:-40800px; }
    }

.. code:: html
    
    ...
      <div id="terrain">

        <!-- Main Body -->
        <div class="container stack-top">
        {% block content %}
        {% endblock content %}
        </div>

      </div>
    ...


