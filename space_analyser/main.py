#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import argparse
import logging
from datetime import datetime

import folderstats

#from lib.scanner import Scanner

# Setup logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    # Create args
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ignore_hidden', required=False, default=True)
    parser.add_argument('--set_name', required=False, default='no-name')
    parsed_args = parser.parse_args()

    logger = logging.getLogger("scanner")
    logger.info('Initializing')
    #logger.info('PARAM:ignore_hidden ' + )

    # Check params
    scan_path = parsed_args.path
    ignore_hidden = parsed_args.ignore_hidden
    output_path = parsed_args.output
    set_name = parsed_args.set_name

    # Source data downloader
    logger.info('Scanning ' + scan_path)

    # Get run timestamp
    timestamp = datetime.now()

    # Scan folders
    df = folderstats.folderstats(scan_path, logger, hash_name='md5', ignore_hidden=ignore_hidden)

    # Annotate table
    df['runtime'] = timestamp.strftime("%Y-%m-%d-%H:%M:%S")
    df['setname'] = set_name

    # Output to file
    df.to_csv(output_path, index=False)

    sys.exit