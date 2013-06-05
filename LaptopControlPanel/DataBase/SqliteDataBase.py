####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2013 Fabrice Salvaire
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
