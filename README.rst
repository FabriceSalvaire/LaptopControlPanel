=========================
LaptopControlPanel V0.1.0
=========================

.. :Info: The home page of LaptopControlPanel is located at http://fabricesalvaire.github.com/LaptopControlPanel

About
-----

LaptopControlPanel is a Python module that provides a Graphical Control Panel for a Lenovo Thinkpad
Laptop and a tool to monitor and manage the battery.

The control panel features:

* switch on/off network interfaces (wifi and bluetooth)
* battery control
* fan control
* switch on/off Nvidia GPU

The battery management tool permits:

* to set the start and stop capacity threshold to charge the battery,
* to switch on battery when AC power is plugged,
* to setup a "peak shift" procedure.

The source of the ACPI calls for the battery management is unknown and comes from the repository
`tpacpi-bat https://github.com/teleshoes/tpacpi-bat`_. The battery is managed by ACPI calls through
the Low Pin Count bus and the Embedded Controler (ASL base ```\_SB.PCI0.LPC.EC.HKEY```).

For reference, this discussion `Laptop shock detection and harddisk protection
http://lkml.indiana.edu/hypermail/linux/kernel/0810.0/2603.html`_ on LKML illustrates the legal
concern for such information.

Source Repository
-----------------

The source code is licensed under GPL V3 and is available on `GitHub
<https://github.com/FabriceSalvaire/LaptopControlPanel>`_.  Also a Python package is available on
`PyPI <http://pypi.python.org/pypi/LaptopControlPanel>`_.

Requirements
------------

* Python 2.7
* PyQt 4.9
* `acpi_call https://github.com/mkottman/acpi_call`_

Building
--------

Download and unpack the source, then run the following commands in a terminal::

  python setup.py build

Running
-------

.. important::
  Actually LaptopControlPanel needs root privileges to manage the hardware.

Load the *acpi_call* module.

Set the terminal environment using::

  source setenv.sh

then run the command::

  bin/laptop-control-panel

.. End
