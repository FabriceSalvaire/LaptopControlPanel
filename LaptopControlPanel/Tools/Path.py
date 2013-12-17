####################################################################################################
# 
# LaptopControlPanel - A Laptop Control Panel
# Copyright (C) 2013 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import os
import types

####################################################################################################

def to_absolute_path(path):

    # Expand ~ . and Remove trailing '/'

    return os.path.abspath(os.path.expanduser(path))

####################################################################################################

def parent_directory_of(file_name, step=1):
    
    directory = file_name
    for i in xrange(step):
        directory = os.path.dirname(directory)
    return directory

####################################################################################################

def find(file_name, directories):
    
    if isinstance(directories, types.StringType):
        directories = (directories,)
    for directory in directories:
        for directory_path, sub_directories, file_names in os.walk(directory):
            if file_name in file_names:
                return os.path.join(directory_path, file_name)

    raise NameError("File %s not found in directories %s" % (file_name, str(directories)))

####################################################################################################

def find_alias(directory, file_names):

    for file_name in file_names:
        absolut_file_name = os.path.join(directory, file_name)
        if os.path.exists(absolut_file_name):
            return absolut_file_name

    raise NameError("Any file in %s found in directory %s" % (str(file_names), directory))
            
####################################################################################################
#
# End
#
####################################################################################################
