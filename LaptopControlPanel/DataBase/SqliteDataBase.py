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

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

####################################################################################################

class SqliteDataBase(object):

    __base__ = None

    _logger = logging.getLogger(__name__)

    ##############################################
    
    def __init__(self, filename, echo=False):

        self._logger.debug("Open SQLite Database %s" % (filename))
    
        self._filename = filename

        create = not os.path.exists(self._filename)

        connection_str = "sqlite:///" + self._filename
        self._engine = create_engine(connection_str, echo=echo)
        self._session_maker = sessionmaker(bind=self._engine)
        self.session = self._session_maker()

        if create:
            self.__base__.metadata.create_all(self._engine)

####################################################################################################
#
# End
#
####################################################################################################
