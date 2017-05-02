#!/usr/bin/python

import sys
import os
import json

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
        for item in os.listdir(directory):
            content.append(PTN.parse(item))

        return content

def main():
    plex_mover = PlexMover()

if __name__ == '__main__':
    main()

