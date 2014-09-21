.. -*- Mode: rst -*-

.. _installation-page:

.. include:: project-links.txt
.. include:: abbreviation.txt

==============
 Installation
==============

Dependencies
------------

LaptopControlPanel requires the following dependencies:

 * Python 2.7
 * PyQt 4.9
 * `acpi_call <https://github.com/mkottman/acpi_call>`_

Installation from PyPi Repository
---------------------------------

LaptopControlPanel is made available on the |Pypi|_ repository at |LaptopControlPanel@pypi|

Run this command to install the last release:

.. code-block:: sh

  pip install LaptopControlPanel

Installation from Source
------------------------

The LaptopControlPanel source code is hosted at |LaptopControlPanel@github|

To clone the Git repository, run this command in a terminal:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/LaptopControlPanel.git

Then to build and install LaptopControlPanel run these commands:

.. code-block:: sh

  python setup.py build
  python setup.py install

.. End
