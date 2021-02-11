#!/usr/bin/env python
# coding: utf-8

from datetime import datetime
import logging

import folderstats

class Scanner:
    def __init__(self, logger):
        # Init
        self.logger = logger

    def scan(self, scan_path, ignore_hidden, set_name, verbose=False):
        # Source data downloader
        self.logger.info('Scanning ' + scan_path)

        # Get run timestamp
        timestamp = datetime.now()

        # Scan folders
        df = folderstats.folderstats(scan_path, self.logger, hash_name='md5', ignore_hidden=ignore_hidden, verbose=verbose)

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

        return df