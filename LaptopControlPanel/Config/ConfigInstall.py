####################################################################################################
# 
# LaptopControlPanel - @ProjectDescription@.
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import os

####################################################################################################

import LaptopControlPanel.Tools.Path as PathTools # due to Path class

####################################################################################################

_this_file = PathTools.to_absolute_path(__file__)

class Path(object):

    module_directory = PathTools.parent_directory_of(_this_file, step=2)
    config_directory = os.path.dirname(_this_file)
    share_directory = os.path.realpath(os.path.join(config_directory, '..', '..', 'share'))

####################################################################################################

class Logging(object):

    default_config_file = 'logging.yml'
    directories = (Path.config_directory,)

    ##############################################

    @staticmethod
    def find(config_file):

        return PathTools.find(config_file, Logging.directories)

####################################################################################################

class Icon(object):

    ##############################################

    @staticmethod
    def find(file_name, size):

        icon_directory = os.path.join(Path.share_directory, 'icons', '%ux%u' % (size, size))
        return PathTools.find(file_name, (icon_directory,))

####################################################################################################
#
# End
#
####################################################################################################
