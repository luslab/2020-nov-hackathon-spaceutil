#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
import logging

import pandas as pd

from lib.scanner import Scanner
from lib.database import Database

def scan(parsed_args):
    scan_path = parsed_args.path
    ignore_hidden = parsed_args.ignore_hidden
    output_path = parsed_args.output
    set_name = parsed_args.set_name
    log_path = None

    if parsed_args.log:
        log_path = parsed_args.log

    logging.basicConfig(filename=log_path, level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("scanner")
    logger.info('Init scan')

    # Call the scanner
    s = Scanner(logger)
    df = s.scan(scan_path, ignore_hidden, set_name)
    
    # Output to file
    df.to_csv(output_path, index=False)

    logger.info('Scan complete: ' + str(len(df)) + ' items')

def testdb(args):
    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("testdb")
    logger.info('Init testdb')

    d = Database(url, usr, pw, db, logger)
    d.test_connection()

    # df = d.get_size_summary()
    # df.to_csv(os.path.join(output_path, 'size_summary.csv'), index=False)

def upload(args):
    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db
    path = parsed_args.path
    log_path = None

    if parsed_args.log:
        log_path = parsed_args.log

    logging.basicConfig(filename=log_path, level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("upload")
    logger.info('Init upload')

    df = pd.read_csv(path)
    d = Database(url, usr, pw, db, logger)
    d.upload_scan(df)

def rebuild(args):
    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("rebuild")
    logger.info('Init rebuild')

    d = Database(url, usr, pw, db, logger)
    d.rebuild_server()

def view(args):
    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db
    view = parsed_args.view_name

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("view")
    logger.info('Init view')

    d = Database(url, usr, pw, db, logger)

    df = pd.DataFrame()
    if view == 'scan_hist':
        df = d.get_scan_hist()
    elif view == 'size_summary':
        df = d.get_size_summary('/Users/cheshic/dev/repos/TOBIAS/')

    if parsed_args.output is not None:
        logger.info('Writing to ' + parsed_args.output)
        df.to_csv(parsed_args.output, index=False)

if __name__ == '__main__':
    # Create command args
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # Functions
    parser_scan = subparsers.add_parser('scan', help='scan help')
    parser_scan.set_defaults(func=scan)
    parser_test_db = subparsers.add_parser('testdb', help='test-db help')
    parser_test_db.set_defaults(func=testdb)
    parser_upload = subparsers.add_parser('upload', help='upload help')
    parser_upload.set_defaults(func=upload)
    parser_rebuild = subparsers.add_parser('rebuild', help='rebuild help')
    parser_rebuild.set_defaults(func=rebuild)
    parser_view = subparsers.add_parser('view', help='view help')
    parser_view.set_defaults(func=view)

    # scan params
    parser_scan.add_argument('--path', required=True)
    parser_scan.add_argument('--output', required=True)
    parser_scan.add_argument('--ignore_hidden', required=False, default=True)
    parser_scan.add_argument('--set_name', required=False, default='no-name')
    parser_scan.add_argument('--log', required=False)

    # test-db params
    parser_test_db.add_argument('--url', required=True)
    parser_test_db.add_argument('--usr', required=True)
    parser_test_db.add_argument('--pw', required=True)
    parser_test_db.add_argument('--db', required=True)

    # upload params
    parser_upload.add_argument('--path', required=True)
    parser_upload.add_argument('--log', required=False)
    parser_upload.add_argument('--url', required=True)
    parser_upload.add_argument('--usr', required=True)
    parser_upload.add_argument('--pw', required=True)
    parser_upload.add_argument('--db', required=True)

    # rebuild params
    parser_rebuild.add_argument('--url', required=True)
    parser_rebuild.add_argument('--usr', required=True)
    parser_rebuild.add_argument('--pw', required=True)
    parser_rebuild.add_argument('--db', required=True)

    # view params
    parser_view.add_argument('--url', required=True)
    parser_view.add_argument('--usr', required=True)
    parser_view.add_argument('--pw', required=True)
    parser_view.add_argument('--db', required=True)
    parser_view.add_argument('--view_name', required=True)
    parser_view.add_argument('--output', required=False)

    # Parse
    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)