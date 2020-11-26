#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from cloudant import couchdb
from cloudant.view import View
from uuid import uuid4

class Database:
    def __init__(self, url, username, password, database, logger):
        # Init
        self.logger = logger
        self.url = url
        self.usr = username
        self.pw = password
        self.db = database

    def create_frame(self, docs):
        df = pd.DataFrame(columns=['_id','_rev','scan_id','path','file_name','size','is_folder','depth','parent','md5','scan_time','elapsed','set_name'])
        for doc in docs:
            df = df.append(doc, ignore_index=True)

        return df

    def test_connection(self):
        with couchdb(self.usr, self.pw, url=self.url) as client:
            print(client.all_dbs())

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
        # Get connection and db
        with couchdb(self.usr, self.pw, url=self.url) as client:
            db = client[self.db]

            selector = {'is_folder': {'$eq': True}}
            docs = db.get_query_result(selector)

            df = self.create_frame(docs)

        return df

# '_id': 'd7f49ca6c92a49128f00c89558cb065c',
# '_rev': '1-ab43f47b524c0ed9cf5bbddbfb2f54e9',
# 'scan_id': 29,
# 'path': '/Users/cheshic/dev/repos/TOBIAS/tobias/__init__.py',
# 'file_name': '__init__',
# 'size': 23,
# 'is_folder': False, 
# 'depth': 1,
# 'parent': 4,
# 'md5': '0ab6e1ae54ddc1cb0d9c3e42549b1ce4', 
# 'scan_time': '2020-11-26-15:40:17', 
# 'elapsed': '00:00:00',
# 'set_name': 'no-name'