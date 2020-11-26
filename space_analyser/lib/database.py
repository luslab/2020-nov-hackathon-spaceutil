#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from cloudant.client import Cloudant

class Database:
    def __init__(self, logger=None, url, username, password):
        # Init
        self.logger = logger

        # Connect to database
        self.client = Cloudant(username, password, url=url)
        self.session = client.session()

        # Log
        logger.info('Username: {0}'.format(session['userCtx']['name'])) if logger
        logger.info('Databases: {0}'.format(client.all_dbs())) if logger

    def __del__(self):
        # Disconnect from the server
        if self.client:
            client.disconnect()