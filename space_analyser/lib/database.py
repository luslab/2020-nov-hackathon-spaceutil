#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import couchdb

class Database:
    def __init__(self, url, username, password, logger):
        # Init
        self.logger = logger
        connect_string = 'http://' + username + ':' + password + '@' + url + '/'

        # Log
        logger.info('Connecting to {0}'.format(connect_string))

        # Connect to db
        self.server = couchdb.Server(connect_string)

    def test_connection(self):
        self.logger.info('CouchDB version {0}'.format(self.server.version()))