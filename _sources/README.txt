=========================
LaptopControlPanel V0.1.0
=========================

.. :Info: The home page of LaptopControlPanel is located at http://fabricesalvaire.github.com/LaptopControlPanel

About
-----

LaptopControlPanel is a Python module that provides a Graphical Control Panel for Lenovo Thinkpad
Laptop and a console tool to monitor and manage the battery. Such functions are not provided by
standard control panels like those of the KDE desktop.

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

Source Repository
-----------------

The source code is licensed under GPL V3 and is available on `GitHub
<https://github.com/FabriceSalvaire/LaptopControlPanel>`_.  Also a Python package is available on
`PyPI <http://pypi.python.org/pypi/LaptopControlPanel>`_.

Requirements
------------

* Python 2.7
* PyQt 4.9
* `acpi_call <https://github.com/mkottman/acpi_call>`_

Building
--------

Download and unpack the source, then run the following commands in a terminal::

  python setup.py build

Running
-------

.. important::
  Actually LaptopControlPanel needs root privileges so as to read and write **/proc** entries.

The *acpi_call* module must be loaded in order to manage the battery.

Set the terminal environment using::

  source setenv.sh

then run the command::

  bin/laptop-control-panel

.. End
