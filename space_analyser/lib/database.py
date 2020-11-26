#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import couchdb
from uuid import uuid4

class Database:
    def __init__(self, url, username, password, database, logger):
        # Init
        self.logger = logger
        connect_string = 'http://' + username + ':' + password + '@' + url + '/'

        # Log
        logger.info('Connecting to {0}'.format(connect_string))

        # Connect to db
        self.server = couchdb.Server(connect_string)
        self.db = self.server[database]

    def test_connection(self):
        self.logger.info('CouchDB version {0}'.format(self.server.version()))

        self.get_size_summary()
        #df.info()

        # for id in self.db:
        #     print(id)

    def upload_scan(self, data):
        self.logger.info('Uploading data...')

        # iterate and save to db
        for index, row in data.iterrows():
            doc = {
                '_id': uuid4().hex,
                'scan_id': row['id'],
                'path': row['path'],
                'file_name': row['name'],
#                'ext': row['extension'],
                'size': row['size'],
                'is_folder': row['folder'],
                'depth': row['depth'],
                'parent': row['parent'],  
                'md5': row['md5'],
                'scan_time': row['scantime'],
                'elapsed': row['elapsed'],
                'set_name': row['setname']
            }
            self.db.save(doc)

    def get_size_summary(self):

        for item in self.db.view('_design/main'):
            print(item)


        # map_fun = '''function(doc) {
        #                 if(doc.date && doc.title) {
        #                     emit(doc.date, doc.title);
        #                 }
        #             }'''