####################################################################################################
# 
# Thinkpad ACPI Battery Control
# Copyright (C) Salvaire Fabrice 2013 
# 
####################################################################################################

import logging
import collections
import os
import subprocess

####################################################################################################

logger = logging.getLogger('battery_control')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info('Start')

####################################################################################################

class DictInitialised(object):
    
    ##############################################

    def __init__(self, **kwargs):

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

####################################################################################################

class AcpiCallDevice(object):

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
        rc = subprocess.check_call(['/sbin/insmod', 'acpi_call'])
        if rc:
            raise NameError("Cannot load module acpi_call")

    ##############################################

    def call(self, call_string):

        with open(self._acpi_call_device, 'w') as device_file:
            logger.debug("Call ACPI Function '%s'" % call_string)
            device_file.write(call_string)
        with open(self._acpi_call_device, 'r') as device_file:
            return_value = device_file.read()
            logger.debug("Call returned '%s'" % return_value)

        return int(return_value, 16)

    ##############################################

    def define_function(self, name, input_arguments, output_arguments):

        return AcpiCallFunction(self, name, input_arguments, output_arguments)

####################################################################################################

class AcpiCallFunction(object):

    # _logger = logging.getLogger(__name__ + '.AcpiCallFunction')

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

        logger.debug(str(values))
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

class BatteryControl(object):

    # LPC means Low Pin Count Bus
    # EC means Embedded Controller
    _asl_base = r'\_SB.PCI0.LPC.EC.HKEY'

    either_both_battery, main_battery, secondary_battery = range(3)

    ##############################################

    def __init__(self):

        self._acpi_call_device = AcpiCallDevice()

        # Peak Shift State

        self._get_peak_shift_state_acpi_call = self._define_function(
            name='PSSG',
            input_arguments=AcpiCallArguments(reserved=31),
            output_arguments=AcpiCallArguments(inhibit_charge_status=0,
                                               reserved1=3,
                                               discharge_with_ac_capability=4,
                                               inhibit_charge_capability=5,
                                               inhibit_charge_auto_reset_capability=6,
                                               reserved2=7,
                                               inhibit_charge_effective_timer=23,
                                               reserved3=30,
                                               error_status=31,
                                               ),
            )

        self._set_peak_shift_state_acpi_call = self._define_function(
            name='PSSS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=0,
                                              timer=23,
                                              reserved2=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        self._set_peak_shift_discharge_state_acpi_call = self._define_function(
            name='PSBS',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              discharge_status=15,
                                              reserved=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Inhibit Charge
        
        self._set_inhibit_charge_state_acpi_call = self._define_function(
            name='BICS',
            input_arguments=AcpiCallArguments(inhibit_charge=0,
                                              reserved1=3,
                                              battery_id=5,
                                              reserved2=7,
                                              timer=23,
                                              reserved3=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Charge Start Threshold

        self._get_charge_start_threshold_acpi_call = self._define_function(
            name='BCTG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(start_treshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_start_threshold_acpi_call = self._define_function(
            name='BCCS',
            input_arguments=AcpiCallArguments(charge_start_capacity=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Charge Stop Threshold
        
        self._get_charge_stop_threshold_acpi_call = self._define_function(
            name='BCSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=0),
            output_arguments=AcpiCallArguments(stop_threshold=7,
                                               capability=8,
                                               can_specify_every_battery=9,
                                               reserved=30,
                                               error_status=31,
                                               ),
            )

        self._set_charge_stop_threshold_acpi_call = self._define_function(
            name='BCSS',
            input_arguments=AcpiCallArguments(stop_threshold=7,
                                              battery_id=9,
                                              reserved=31,
                                              ),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

        # Battery Discharge State

        self._get_discharge_state_acpi_call = self._define_function(
            name='BDSG',
            input_arguments=AcpiCallArguments(battery_id=7,
                                              reserved=31),
            output_arguments=AcpiCallArguments(discharge_status=0,
                                               break_by_ac_detaching=1,
                                               reserved1=7,
                                               discharge_capability=8,
                                               can_specify_every_battery=9,
                                               can_break=10,
                                               reserved2=30,
                                               error_status=31,
                                               ),
            )

        self._set_discharge_state_acpi_call = self._define_function(
            name='BDSS',
            input_arguments=AcpiCallArguments(force_discharge=0,
                                              break_by_ac_detaching=1,
                                              reserved1=7,
                                              battery_id=9,
                                              reserved2=31),
            output_arguments=AcpiCallArguments(reserved=30, error_status=31),
            )

    ##############################################

    def _define_function(self, name, input_arguments, output_arguments):

        return self._acpi_call_device.define_function(self._asl_base + '.' + name,
                                                      input_arguments, output_arguments)

    ##############################################

    def _check_battery_id_for_reading(self, battery_id):

        if battery_id == self.either_both_battery:
            raise ValueError("Can't specify either or both battery for reading.")

    ##############################################

    def _check_charge_threshold(self, threshold=None):

        if threshold is None:
            threshold = 0
        elif not (1 <= threshold <= 99):
            raise ValueError("Wrong charge treshold value " + str(threshold))
        return threshold

    ##############################################

    def _check_error_status(self, result):

        if result.error_status:
            raise ValueError("ACPI call failed")

    ##############################################

    def set_start_threshold(self, battery_id=main_battery, threshold=None):

        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_start_threshold_acpi_call.call(battery_id=battery_id,
                                                                 charge_start_capacity=threshold,
                                                                 )
        self._check_error_status(result)

    ##############################################

    def set_stop_threshold(self, battery_id=main_battery, threshold=None):

        threshold = self._check_charge_threshold(threshold)
        result = self._set_charge_stop_threshold_acpi_call.call(battery_id=battery_id,
                                                                charge_stop_capacity=threshold,
                                                                )
        self._check_error_status(result)

    ##############################################

    def get_start_threshold(self, battery_id=main_battery):
        self._check_battery_id_for_reading(battery_id)
        return self._get_charge_start_threshold_acpi_call.call(battery_id=battery_id)

    ##############################################

    def get_stop_threshold(self, battery_id=main_battery):
        self._check_battery_id_for_reading(battery_id)
        return self._get_charge_stop_threshold_acpi_call.call(battery_id=battery_id)
    
    ##############################################

    @property
    def inhibit_charge(self):
        call = 'BICS'

    @inhibit_charge.setter
    def inhibit_charge(self, value):
        call = 'BICG'        

    ##############################################

    def set_force_discharge(self, battery_id=main_battery, force_discharge=True, break_by_ac_detaching=False):
        result = self._set_discharge_state_acpi_call.call(battery_id=battery_id,
                                                          force_discharge=force_discharge,
                                                          break_by_ac_detaching=break_by_ac_detaching,
                                                          )
        self._check_error_status(result)

    ##############################################       

    def get_force_discharge(self, battery_id=main_battery):
        self._check_battery_id_for_reading(battery_id)
        result = self._get_discharge_state_acpi_call.call(battery_id=battery_id)

    ##############################################

    @property
    def peak_shift_state(self):
        call = 'PSSS'

    def get_peak_shift_state(self):
        result = self._get_peak_shift_state_acpi_call.call()

####################################################################################################

if __name__ == "__main__":

    battery_control = BatteryControl()

    # battery_control.set_start_threshold(battery_control.main_battery, threshold=40)
    # battery_control.set_stop_threshold(battery_control.main_battery, threshold=80)
    battery_control.get_start_threshold(battery_control.main_battery)
    battery_control.get_stop_threshold(battery_control.main_battery)

    battery_control.get_force_discharge(battery_control.main_battery)
    battery_control.get_peak_shift_state()
    battery_control.set_force_discharge(force_discharge=False)
    battery_control.get_force_discharge(battery_control.main_battery)
    battery_control.get_peak_shift_state()

####################################################################################################
# 
# End
# 
####################################################################################################
