.. -*- Mode: rst -*-

.. _testing-page:

=========
 Testing
=========

.. image:: /images/screenshot1.png
  :scale: 50%

.. image:: /images/screenshot2.png
  :scale: 50%

.. important::
  Actually LaptopControlPanel needs root privileges so as to read and write **/proc** entries.

The *acpi_call* module must be loaded in order to manage the battery.

Set the terminal environment using::

  source setenv.sh

then run the command::

  bin/laptop-control-panel

.. End
