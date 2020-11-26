#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import argparse
import logging
import datetime
import os

#from lib.scanner import Scanner

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

if __name__ == '__main__':
    # Create args
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parsed_args = parser.parse_args()

    logger = logging.getLogger("scanner")
    logger.info('Initializing')

    # Check params
    scan_path = parsed_args.path

    # Source data downloader
    logger.info('Scanning ' + scan_path)
    sys.exit