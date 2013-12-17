####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import StringIO
import sys
import traceback

####################################################################################################

from LaptopControlPanel.Tools.Singleton import singleton

####################################################################################################

def format_exception(exception_type, exception_value, exception_traceback):

    """ Format an exception to string. """

    # traceback.format_exc()
    traceback_string_io = StringIO.StringIO()
    traceback.print_exception(exception_type, exception_value, exception_traceback, file=traceback_string_io)

    return traceback_string_io.getvalue()

####################################################################################################

@singleton
class DispatcherExceptionHook(object):

    """ DispatcherExceptionHook install an exception hook in the Python interpreter. This class is a
    singleton and follows the Observer Pattern.  When an exception is raised, it is catched by the
    hook, that calls the method :meth:`notify` for each registered observer.
    """

    ##############################################

    def __init__(self):

        self._observers = []

        sys.excepthook = self._exception_hook

    ##############################################

    def __iter__(self):

        return iter(self._observers)

    ##############################################

    def __getitem__(self, exception_hook_class):

        for observer in self:
            if isinstance(observer, exception_hook_class):
                return observer
        else:
            return None

    ##############################################

    def register_observer(self, observer):

        """ Register an observer, that must have a :meth:`notify` method. """

        self._observers.append(observer)

    ##############################################

    def _exception_hook(self, exception_type, exception_value, exception_traceback):
     
        for observer in self:
            observer.notify(exception_type, exception_value, exception_traceback)

####################################################################################################

class ExceptionHook(object):

    ##############################################

    def __init__(self, context=''):

        self.context = context

        # DispatcherExceptionHook().register_observer(self)

####################################################################################################

class StderrExceptionHook(ExceptionHook):

    """ Log exception on stderr. """

    _line_width = 80
    _line = '='*_line_width

    ##############################################

    def __init__(self, context=''):

        super(StderrExceptionHook, self).__init__(context)

    ##############################################

    def notify(self, exception_type, exception_value, exception_traceback):

        print >>sys.stderr, self._line, '\n'
        print >>sys.stderr, 'StderrExceptionHook'.center(self._line_width), '\n'
        # traceback.print_exc()
        traceback.print_exception(exception_type, exception_value, exception_traceback)
        print >>sys.stderr, '\n', self._line 

####################################################################################################
#
# End
#
####################################################################################################
