.. -*- Mode: rst -*-

.. -*- Mode: rst -*-

..
   |LaptopControlPanelUrl|
   |LaptopControlPanelHomePage|_
   |LaptopControlPanelDoc|_
   |LaptopControlPanel@github|_
   |LaptopControlPanel@readthedocs|_
   |LaptopControlPanel@readthedocs-badge|
   |LaptopControlPanel@pypi|_

.. |ohloh| image:: https://www.openhub.net/accounts/230426/widgets/account_tiny.gif
   :target: https://www.openhub.net/accounts/fabricesalvaire
   :alt: Fabrice Salvaire's Ohloh profile
   :height: 15px
   :width:  80px

.. |LaptopControlPanelUrl| replace:: http://fabricesalvaire.github.io/LaptopControlPanel

.. |LaptopControlPanelHomePage| replace:: LaptopControlPanel Home Page
.. _LaptopControlPanelHomePage: http://fabricesalvaire.github.io/LaptopControlPanel

.. |LaptopControlPanelDoc| replace:: LaptopControlPanel Documentation
.. _LaptopControlPanelDoc: http://laptopcontrolpanel.readthedocs.org/en/latest

.. |LaptopControlPanel@readthedocs-badge| image:: https://readthedocs.org/projects/laptopcontrolpanel/badge/?version=latest
   :target: http://laptopcontrolpanel.readthedocs.org/en/latest

.. |LaptopControlPanel@github| replace:: https://github.com/FabriceSalvaire/LaptopControlPanel
.. .. _LaptopControlPanel@github: https://github.com/FabriceSalvaire/LaptopControlPanel

.. |LaptopControlPanel@readthedocs| replace:: http://laptopcontrolpanel.readthedocs.org
.. .. _LaptopControlPanel@readthedocs: http://laptopcontrolpanel.readthedocs.org

.. |LaptopControlPanel@pypi| replace:: https://pypi.python.org/pypi/LaptopControlPanel
.. .. _LaptopControlPanel@pypi: https://pypi.python.org/pypi/LaptopControlPanel

.. |Build Status| image:: https://travis-ci.org/FabriceSalvaire/LaptopControlPanel.svg?branch=master
   :target: https://travis-ci.org/FabriceSalvaire/LaptopControlPanel
   :alt: LaptopControlPanel build status @travis-ci.org

.. End
.. -*- Mode: rst -*-

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

.. End

====================
 LaptopControlPanel
====================

The official LaptopControlPanel Home Page is located at |LaptopControlPanelUrl|

The latest documentation build from the git repository is available at readthedocs.org |LaptopControlPanel@readthedocs-badge|

Written by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_.

|Build Status|

-----

.. image:: https://raw.github.com/FabriceSalvaire/LaptopControlPanel/master/doc/sphinx/source/images/screenshot1-scaled.png
.. image:: https://raw.github.com/FabriceSalvaire/LaptopControlPanel/master/doc/sphinx/source/images/screenshot2-scaled.png

.. -*- Mode: rst -*-


==============
 Introduction
==============

LaptopControlPanel is a Python module that provides a Graphical Control Panel for Lenovo Thinkpad
Laptop and a console tool to monitor and manage the battery. Such functions are not provided by
standard control panels like those of the KDE desktop.

It was used on a Lenovo Thinkpad T430 model. The ACPI calls could not work on more recent models.

The source code is licensed under GPL V3.

.. warning::
  This Python module uses ACPI calls and low level hardware functions. A miss use of these tools can
  crash the computer.

The control panel features:

* switch on/off network interfaces (wifi and bluetooth)
* switch on/off Nvidia GPU using ``/proc/acpi/bbswitch``
* fan control using **thinkpad-acpi** module and ``/proc/acpi/ibm/fan``
* battery control through ACPI calls

The battery management tool permits:

* to set the start and stop capacity threshold to charge the battery,
* to switch on battery when AC power is plugged,
* to setup a "peak shift" procedure.

Some usages of these functions are:

* to switch off the Nvidia GPU to save battery
* to speed-up the fan to cool the hard drive located under the left hand

The source of the ACPI calls for the battery management is unknown and comes from the repository
`tpacpi-bat <https://github.com/teleshoes/tpacpi-bat>`_. For reference, this discussion `Laptop
shock detection and harddisk protection
<http://lkml.indiana.edu/hypermail/linux/kernel/0810.0/2603.html>`_ on LKML illustrates the legal
concern for such information.

The battery is managed by ACPI calls through the Low Pin Count bus and the Embedded Controller (ASL
base is ``\_SB.PCI0.LPC.EC.HKEY``). ACPI is an abstraction layer to set and get registers on the
computer busses. The (`acpi_call <https://github.com/mkottman/acpi_call>`_) module, which is not
included in the kernel, is required to perform these calls. This module must be used carefully.

.. End

.. -*- Mode: rst -*-

.. _installation-page:


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

.. End
