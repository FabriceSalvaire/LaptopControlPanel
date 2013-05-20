####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) 2013 
# 
####################################################################################################

####################################################################################################

import logging
import os
import subprocess

####################################################################################################

from LaptopControlPanel.Tools.DictTools import DictInitialised

####################################################################################################

class AcpiCallDevice(object):

    _logger = logging.getLogger(__name__ + '.AcpiCallDevice')

    _acpi_call_device = '/proc/acpi/call'

    ##############################################

    def __init__(self):

        if not self._acpi_call_device_exists():
            self._load_acpi_call_module()
        if not self._acpi_call_device_exists():
            raise NameError("Could not find %s. Is module acpi_call loaded?" % self._acpi_call_device)

    ##############################################

    def _acpi_call_device_exists(self):

        return os.path.exists(self._acpi_call_device)

    ##############################################

    def _load_acpi_call_module(self):

        # kernel_version = subprocess.check_outpout(['/bin/uname', '-r'])
        # module_path = os.path.join('lib', 'modules', kernel_version, 'extra', 'acpi_call.ko')
        self._logger.debug("Load module acpi_call")
        rc = subprocess.check_call(['/sbin/modprobe', 'acpi_call'])
        if rc:
            raise NameError("Cannot load module acpi_call")

    ##############################################

    def call(self, call_string):

        with open(self._acpi_call_device, 'w') as device_file:
            self._logger.debug("Call ACPI Function '%s'" % call_string)
            device_file.write(call_string)
        with open(self._acpi_call_device, 'r') as device_file:
            return_value = device_file.read()
            self._logger.debug("Call returned '%s'" % return_value)

        return int(return_value, 16)

    ##############################################

    def define_function(self, name, input_arguments, output_arguments):

        return AcpiCallFunction(self, name, input_arguments, output_arguments)

####################################################################################################

class AcpiCallFunction(object):

    _logger = logging.getLogger(__name__ + '.AcpiCallFunction')

    ##############################################

    def __init__(self, acpi_call_device, acpi_path, input_arguments, output_arguments):

        self._acpi_call_device = acpi_call_device
        self._acpi_path = acpi_path
        self._input_arguments = input_arguments
        self._output_arguments = output_arguments

    ##############################################

    def call(self, **kwargs):

        double_word = self._input_arguments.encode(**kwargs)
        call_string = self._acpi_path + ' ' + hex(double_word)
        double_word = self._acpi_call_device.call(call_string)
        return self._output_arguments.decode(double_word)
    
####################################################################################################

class AcpiCallArguments(object):

    _logger = logging.getLogger(__name__ + '.AcpiCallArguments')

    ##############################################

    def __init__(self, **kwargs):

        items = sorted(kwargs.items(), cmp=lambda a, b: cmp(a[1], b[1]))
        self._arguments = []
        lower_bit = 0
        for argument_name, upper_bit in items:
            self._arguments.append(AcpiCallArgument(argument_name, upper_bit, lower_bit))
            lower_bit = upper_bit + 1
        self._argument_names = [argument.name for argument in self._arguments]

    ##############################################

    def encode(self, **kwargs):

        for given_argument in kwargs:
            if given_argument not in self._argument_names:
                raise ValueError("Wrong argument %s" % (given_argument))

        double_word = 0
        for argument in self._arguments:
            if argument.name in kwargs:
                value = kwargs[argument.name]
            else:
                value = 0
            double_word += argument.encode(value)

        return double_word

    ##############################################

    def decode(self, double_word):

        values = {}
        for argument in self._arguments:
            value = argument.decode(double_word)
            if argument.name.startswith('reserved'):
                if value != 0:
                    raise ValueError("Reserved %s bits are non-zero %u" % (argument.name, value))
            else:
                values[argument.name] = value

        self._logger.debug(str(values))

        return DictInitialised(**values)

####################################################################################################

class AcpiCallArgument(object):

    ##############################################

    def __init__(self, name, upper_bit, lower_bit):
        
        self.name = name
        self.upper_bit = upper_bit
        self.lower_bit = lower_bit
        self.number_of_bits = upper_bit - lower_bit +1

    ##############################################

    def _check_value(self, value):

        if self.number_of_bits == 1:
            value= bool(value)
        value = int(value)
        if value >= 2**self.number_of_bits:
            raise ValueError("Out of range")

        return value

    ##############################################

    def encode(self, value):

        return self._check_value(value) << self.lower_bit

    ##############################################

    def decode(self, double_word):

        value = (double_word >> self.lower_bit) & (2**self.number_of_bits -1)
        if self.number_of_bits == 1:
            return bool(value)
        else:
            return value

####################################################################################################
# 
# End
# 
####################################################################################################
