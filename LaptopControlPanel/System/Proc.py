####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import os
import types

####################################################################################################

class ProcFile(object):

    ##############################################

    @staticmethod
    def compile_format_list(format_list):

        format_list = list(format_list)
        if not isinstance(format_list[0], str):
            format_list = [''] + format_list
        if not isinstance(format_list[-1], str):
            format_list = format_list + ['']
            
        separator = True
        for item in format_list:
            if separator:
                if not isinstance(item, str):
                    raise ValueError("A separator string is expected")
            elif not isinstance(item, type):
                raise ValueError("A type is expected")
            separator = not separator

        # check separator is not ''

        return format_list

    ##############################################

    @staticmethod
    def join(arg1, **args):
        return os.path.join('/proc', arg1, **args)

    ##############################################

    @staticmethod
    def parse_line(compiled_format_list, line):

        first_separator = compiled_format_list[0]
        if line.startswith(first_separator):
            line = line[len(first_separator):]
        else:
            raise ValueError()

        number_of_fields = len(compiled_format_list)/2 # +1 doesn't matter

        fields = []
        for i in xrange(number_of_fields):
            index = 2*i +1
            field_type, separator = compiled_format_list[index:index+2]
            if separator:
                separator_location = line.find(separator)
                if not separator_location: # must be > 0
                    raise ValueError()
            else:
                separator_location = None
            field_text = line[:separator_location]
            field = field_type(field_text)
            fields.append(field)
            if separator_location:
                line = line[separator_location + len(separator):]

        return fields

####################################################################################################

class ProcOneLineFile(ProcFile):

    __format_list__= ()
    __file_name__ = None

    ##############################################

    def __init__(self):

        self._path = self.join(self.__file_name__)
        self._compiled_format_list = self.compile_format_list(self.__format_list__)

    ##############################################

    def read(self):

        with open(self._path, 'r') as f:
            line = f.readline().rstrip()
        return self.parse_line(self._compiled_format_list, line)

####################################################################################################

class LoadAverage(ProcOneLineFile):

    # number_of_job_1_min number_of_job_5_min number_of_job_15_min number_of_runnable_entities/number_of_job_entities last_pid
    __format_list__= (float, ' ', float, ' ', float, ' ', int, '/', int, ' ', int)
    __file_name__ = 'loadavg'
                        
####################################################################################################
# 
# End
# 
####################################################################################################
