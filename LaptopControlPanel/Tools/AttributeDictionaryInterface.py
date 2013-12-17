####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

class ExtendedDictionaryInterface(dict):

    """ This class implements an extended dictionary interface.

      :attr:`clear`
      :attr:`copy`
      :attr:`fromkeys`
      :attr:`get`
      :attr:`has_key`
      :attr:`items`
      :attr:`iteritems`
      :attr:`iterkeys`
      :attr:`itervalues`
      :attr:`keys`
      :attr:`pop`
      :attr:`popitem`
      :attr:`setdefault`
      :attr:`update`
      :attr:`values`
      :attr:`viewitems`
      :attr:`viewkeys`
      :attr:`viewvalues`

    """

    ##############################################
    
    def __setitem__(self, key, value):

        # Fixme: ?

        if key not in self and key not in self.__dict__:
            super(ExtendedDictionaryInterface, self).__setitem__(key, value)
            self.__dict__[key] = value
        else:
            raise KeyError

####################################################################################################

class ReadOnlyAttributeDictionaryInterface(object):

    """ This class implements a read-only attribute and dictionary interface. """

    ##############################################
    
    def __init__(self):

        object.__setattr__(self, '_dictionary', dict())

    ##############################################
    
    def __getattr__(self, name):

        """ Get the value from its name. """

        return self._dictionary[name]

    ##############################################

    __getitem__ = __getattr__

    ##############################################
    
    def __iter__(self):

        """ Iterate over the dictionary. """

        return self.iterkeys()

    ##############################################
    
    def iteritems(self):

        return self._dictionary.iteritems()

    ##############################################
    
    def iterkeys(self):

        return self._dictionary.iterkeys()

    ##############################################
    
    def itervalues(self):

        return self._dictionary.itervalues()

    ##############################################
    
    def __contains__(self, name):

        """ Test if *name* is in the dictionary. """

        return name in self._dictionary

    ##############################################
    
    def __setattr__(self, name, value):

        raise NotImplementedError

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterface(ReadOnlyAttributeDictionaryInterface):

    """ This class implements an attribute and dictionary interface. """

    ##############################################
    
    def __setattr__(self, name, value):

        """ Set the value from its name. """

        self._dictionary[name] = value

    ##############################################

    __setitem__ = __setattr__

####################################################################################################

class AttributeDictionaryInterfaceDescriptor(AttributeDictionaryInterface):

    ##############################################
    
    def _get_descriptor(self, name):

        return self._dictionary[name]

    ##############################################
    
    def __getattr__(self, name):

        return self._get_descriptor(name).get()

    ##############################################
    
    def __setattr__(self, name, value):

        return self._get_descriptor(name).set(value)

    ##############################################

    __getitem__ = __getattr__
    __setitem__ = __setattr__

####################################################################################################
# 
# End
# 
####################################################################################################
