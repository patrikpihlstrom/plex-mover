#!/usr/bin/python

import sys
import os
import json
from itertools import ifilterfalse

import PTN

class PlexMover:
    config = None

    def __init__(self, test_mode = False):
        if test_mode == True:
            self.config = self.parse_config(os.path.dirname(os.path.abspath(__file__)) + '/test/dummy_config.json');
        else:
            self.config = self.parse_config(os.path.dirname(os.path.abspath(__file__)) + '/config.json');

    def parse_config(self, file):
        with open(file) as config:
            return json.load(config)

        return False

    def get_content_in_directory(self, directory):
        content = []
        keys = ['title', 'season', 'episode']
        for item in os.listdir(directory):
            parsed = PTN.parse(item)

            # get rid of the useless stuff
            for key in list(parsed):
                if key not in keys:
                    del parsed[key]

            if len(parsed) > 0:
                content.append(parsed)

        return content

def main():
    plex_mover = PlexMover()

if __name__ == '__main__':
    main()

