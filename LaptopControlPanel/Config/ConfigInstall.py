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

    size = '32x32'
    icon_directory = os.path.join(Path.share_directory, 'icons', size)
    
    ##############################################

    @staticmethod
    def find(file_name):

        return PathTools.find(file_name, (Icon.icon_directory,))

####################################################################################################
#
# End
#
####################################################################################################
