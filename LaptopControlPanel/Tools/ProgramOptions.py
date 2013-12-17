####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import argparse

####################################################################################################

from .Path import to_absolute_path

####################################################################################################

class PathAction(argparse.Action):

    ##############################################

    def __call__(self, parser, namespace, values, option_string=None):

        # print '%r %r %r' % (namespace, values, option_string)
        if values is not None:
            if isinstance(values, list):
                absolute_path = [to_absolute_path(x) for x in values]
            else:    
                absolute_path = to_absolute_path(values)
        else:
            absolute_path = None
        setattr(namespace, self.dest, absolute_path)

####################################################################################################
#
# End
#
####################################################################################################
