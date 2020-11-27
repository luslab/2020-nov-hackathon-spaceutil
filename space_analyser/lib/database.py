#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from cloudant import couchdb
from cloudant.view import View
from uuid import uuid4

class Database:
    def __init__(self, url, username, password, database, logger):
        self.logger = logger
        self.url = url
        self.usr = username
        self.pw = password
        self.db = database
        self.hist_db = database + '_hist'

    def test_connection(self):
        self.logger.info('Testing db connection...')
        self.logger.info('URL: ' + self.url)
        self.logger.info('USR: ' + self.usr)
        self.logger.info('PW: ' + self.pw)
        with couchdb(self.usr, self.pw, url=self.url) as client:
            self.logger.info('Connected')
            self.logger.info('Available databases: ' + str(client.all_dbs()))

    def rebuild_server(self):
        self.logger.info('Rebuilding server...')

        db_name = self.db
        db_hist_name = self.db + '_hist'

        with couchdb(self.usr, self.pw, url=self.url) as client:
            db_list = client.all_dbs()

            self.logger.info('Deleting existing databases')
            if db_name in db_list:
                client.delete_database(db_name)
            if db_hist_name in db_list:
                client.delete_database(db_hist_name)

            self.logger.info('Creating new databases')
            db = client.create_database(db_name)
            hist_db = client.create_database(db_hist_name)

            self.logger.info('Verifying new databases')
            if db.exists():
                self.logger.info(db_name + ' exists')
            if hist_db.exists():
                self.logger.info(db_hist_name + ' exists')

        self.logger.info('Rebuild complete')
 
    def create_doc_from_row(self, row, hist_id):
        return {
            '_id': uuid4().hex,
            'scan_id': hist_id,
            'item_id': row['id'],
            'path': row['path'],
            'file_name': row['name'],
# #           'ext': row['extension'],
            'size': row['size'],
            'is_folder': row['folder'],
            'depth': row['depth'],
            'parent': row['parent'],  
            'md5': row['md5'],
            'scan_time': row['scantime'],
            'elapsed': row['elapsed'],
            'set_name': row['setname']
        }

    def create_doc_hist_from_row(self, row):
        return {
            '_id': uuid4().hex,
            'scan_time': row['scantime'],
            'elapsed': row['elapsed']
        }

    def upload_scan(self, data):
        self.logger.info('Uploading data...')

        data.fillna("",inplace=True)

        with couchdb(self.usr, self.pw, url=self.url) as client:
            db = client[self.db]
            db_hist = client[self.hist_db]

            for index, row in data.iterrows():
                if index == 0:
                    doc_hist = self.create_doc_hist_from_row(row)
                    db_hist.create_document(doc_hist)

                doc = self.create_doc_from_row(row, doc_hist['_id'])
                db.create_document(doc)
                
        self.logger.info('Upload complete')

    def create_scan_items_from_docs(self, docs):
        df = pd.DataFrame(columns=['_id','_rev','scan_id','item_id','path','file_name','size','is_folder','depth','parent','md5','scan_time','elapsed','set_name'])
        for doc in docs:
            df = df.append(doc, ignore_index=True)

        return df

    def create_scan_hist_items_from_docs(self, docs):
        df = pd.DataFrame(columns=['_id','scan_time','elapsed'])
        for doc in docs:
            df = df.append(doc, ignore_index=True)

        return df

    def get_all_docs(self, db_name):
        docs = []
        with couchdb(self.usr, self.pw, url=self.url) as client:
            db = client[db_name]
            for doc in db:
                docs.append(doc)

        return docs

    def get_docs_from_selector(self, selector):
        with couchdb(self.usr, self.pw, url=self.url) as client:
            db = client[self.db]
            docs = db.get_query_result(selector)
            df = self.create_scan_items_from_docs(docs)
            return df

    def get_scan_hist(self):
        docs = self.get_all_docs(self.hist_db)
        df = self.create_scan_hist_items_from_docs(docs)
        df['scan_time']= pd.to_datetime(df['scan_time'])
        return df

    def get_latest_scan_date(self):
        df = self.get_scan_hist()
        return df['scan_time'].max()

    def get_latest_scan_data(self):
        last_scan = self.get_latest_scan_date()
        selector = {'scan_time': {'$eq': last_scan.strftime("%Y-%m-%d-%H:%M:%S")}}
        df = self.get_docs_from_selector(selector)

        return df

    # https://stackoverflow.com/a/1094933
    def sizeof_fmt(num, suffix='B'):
        for unit in ['K','M','G','T','P','E','Z']:
            if abs(num) < 1024.0:
                return "%3.1f%s%s" % (num, unit, suffix)
            num /= 1024.0
        return "%.1f%s%s" % (num, 'Y', suffix)

    def get_size_summary(self, root):
        self.logger.info('Requesting size summary for ' + root)

        df = self.get_latest_scan_data()

        # Get parent id of the root position
        root_parent = df.query('path==' + root)['item_id'].iloc[0]
        
        # Get all folders with parent of root
        df_folders = df.query('parent==' + str(root_parent) + ' and is_folder==True')

        # Convert sizes
        #df_folders['size_str'] = df['size'].apply(lambda value: self.sizeof_fmt(int(value)))

        # Subset
        df_folders = df_folders[['file_name', 'size']]
        df_folders = df_folders.sort_values(['size'], ascending=[False])

        self.logger.info('Request complete: ' + str(len(df_folders)) + ' items')

        return df_folders