####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

import types

####################################################################################################

def init_default_key(d, **kwargs):

    """ Complete the dict *d* by the dict *kwargs*. """

    for key, value in kwargs.items():
        if key not in d:
            d[key] = value 

####################################################################################################
            
class DictInitialised(object):

    """ This ABC class implements a class initialised by a dict.

    The required attributes are provided by the class attribute '''__REQUIRED_ATTRIBUTES__''' tuple
    and the optional attributes are provided by the class attribute '''__DEFAULT_ATTRIBUTES__'''
    dict where keys define the attribute names and values provide a default value functor.
    """
    
    __REQUIRED_ATTRIBUTES__ = ()
    __DEFAULT_ATTRIBUTES__ = {}
    
    ##############################################

    def __init__(self, **kwargs):

        for key in self.__REQUIRED_ATTRIBUTES__:
            if key in kwargs:
                setattr(self, key, kwargs[key])
            else:
                raise NameError('%s attribute is required' % (key))    

        for key, default_value in self.__DEFAULT_ATTRIBUTES__.items():
            if key in kwargs:
                value = kwargs[key]
            else:
                if isinstance(default_value, types.FunctionType):
                    value = default_value()
                else:
                    value = default_value
            setattr(self, key, value)
            
####################################################################################################
#
# End
#
####################################################################################################

