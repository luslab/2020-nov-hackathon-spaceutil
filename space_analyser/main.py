#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
import logging

from lib.scanner import Scanner
from lib.database import Database

def scan(parsed_args):
    # Check params
    scan_path = parsed_args.path
    ignore_hidden = parsed_args.ignore_hidden
    output_path = parsed_args.output
    set_name = parsed_args.set_name
    upload = parsed_args.upload
    log_path = None

    print(upload)

    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db

    if parsed_args.log:
        log_path = parsed_args.log

    logging.basicConfig(filename=log_path, level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("scanner")
    logger.info('Init')

    # Call the scanner
    s = Scanner(logger)
    df = s.scan(scan_path, output_path, ignore_hidden, set_name)

    if upload == 'true':
        d = Database(url, usr, pw, db, logger)
        d.upload_scan(df)

def testdb(args):
    url = parsed_args.url
    usr = parsed_args.usr
    pw = parsed_args.pw
    db = parsed_args.db

    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("testdb")
    logger.info('Init')

    d = Database(url, usr, pw, db, logger)
    d.test_connection()

if __name__ == '__main__':
    # Create command args
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command help')

    # Functions
    parser_scan = subparsers.add_parser('scan', help='scan help')
    parser_scan.set_defaults(func=scan)
    parser_test_db = subparsers.add_parser('testdb', help='test-db help')
    parser_test_db.set_defaults(func=testdb)

    # scan params
    parser_scan.add_argument('--path', required=True)
    parser_scan.add_argument('--output', required=True)
    parser_scan.add_argument('--ignore_hidden', required=False, default=True)
    parser_scan.add_argument('--upload', required=False, default=False)
    parser_scan.add_argument('--set_name', required=False, default='no-name')
    parser_scan.add_argument('--log', required=False)

    parser_scan.add_argument('--url', required=False)
    parser_scan.add_argument('--usr', required=False)
    parser_scan.add_argument('--pw', required=False)
    parser_scan.add_argument('--db', required=False)

    # test-db params
    parser_test_db.add_argument('--url', required=True)
    parser_test_db.add_argument('--usr', required=True)
    parser_test_db.add_argument('--pw', required=True)
    parser_test_db.add_argument('--db', required=True)

    # Parse
    parsed_args = parser.parse_args()
    parsed_args.func(parsed_args)