#!/usr/bin/python

import sys
import os
import json
import sys
import shutil
from itertools import ifilterfalse

import PTN

class PlexMover:
    config = None
    test_mode = False

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
        content = {}
        keys = ['title', 'season', 'episode']
        for item in os.listdir(directory):
            parsed = PTN.parse(item)

            # get rid of the useless stuff
            for key in list(parsed):
                if key not in keys:
                    del parsed[key]

            if len(parsed) > 0:
                content[item] = parsed

        return content

    def move_content(self, src, content):
        complete_dir = self.config['transmission']['complete']
        tv_dir = self.config['plex']['libraries']['tv']
        movies_dir = self.config['plex']['libraries']['movies']
        _src = str(complete_dir+src)
        if 'episode' in content:
            dest = tv_dir+str(content['title'])+'/Season '+str(content['season'])+'/'+src
        else:
            dest = movies_dir+src

        # is this cheating?
        if self.test_mode:
            shutil.move(os.getcwd()+_src, os.getcwd()+dest)
        else:
            shutil.move(_src, dest)

def main():
    plex_mover = PlexMover()
    complete_dir = plex_mover.config['transmission']['complete']
    content = plex_mover.get_content_in_directory(complete_dir)
    choice = None
    choices = []
    for directory in content.iterkeys():
        choices.append(directory)

    if len(choices) == 0:
        return

    while choice == None:
        index = 0
        for directory in content.iterkeys():
            print '['+str(index)+'] - '+directory
            index = index + 1

        choice = raw_input('^ select an item ^: ')
        if len(choice) == 0:
            choice = None
            continue
        elif choice == '*':
            continue
        else:
            choice = int(choice)

        if choice >= 0 and choice < len(choices):
            pass
        else:
            choice = None

    if choice == '*':
        for key, val in content.iteritems():
            plex_mover.move_content(key, val)
    else:
        plex_mover.move_content(choices[choice], content[choices[choice]])

if __name__ == '__main__':
    main()

