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



if __name__ == '__main__':
    # Create args
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ignore_hidden', required=False, default=True)
    parser.add_argument('--set_name', required=False, default='no-name')
    parser.add_argument('--log', required=False)
    parsed_args = parser.parse_args()

    # Check params
    scan_path = parsed_args.path
    ignore_hidden = parsed_args.ignore_hidden
    output_path = parsed_args.output
    set_name = parsed_args.set_name
    log_path = None

    if parsed_args.log:
        log_path = parsed_args.log

    logging.basicConfig(filename=log_path, level=os.environ.get("LOGLEVEL", "INFO"))
    logger = logging.getLogger("scanner")
    #logger.info('PARAM:ignore_hidden ' + )

    # Source data downloader
    logger.info('Scanning ' + scan_path)

    # Get run timestamp
    timestamp = datetime.now()

    # Scan folders
    df = folderstats.folderstats(scan_path, logger, hash_name='md5', ignore_hidden=ignore_hidden)

    # Calc time elapsed
    time_delta = (datetime.now() - timestamp)
    total_seconds = time_delta.total_seconds()
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

    # Annotate table
    df['scantime'] = timestamp.strftime("%Y-%m-%d-%H:%M:%S")
    df['elapsed'] = elapsed
    df['setname'] = set_name

    # Output to file
    df.to_csv(output_path, index=False)

    sys.exit