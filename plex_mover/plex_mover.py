#!/usr/bin/python

import sys
import os
import json
import sys
import shutil
from itertools import ifilterfalse
from os.path import expanduser

import PTN

class PlexMover:
    config = None
    test_mode = False

    def __init__(self, test_mode = False):
        here = os.path.dirname(os.path.abspath(__file__))
        if test_mode == True:
            self.test_mode = True
            self.config = self.parse_config(os.getcwd() + '/dummy_config.json');
        elif os.path.exists(here + '/config.json'):
            self.config = self.parse_config(here + '/config.json');
        else:
            raise ValueError('No configuration file found.')

    def parse_config(self, file):
        with open(file) as config:
            return json.load(config)

        return False

    def get_content_in_directory(self, directory):
        content = {}
        keys = ['title', 'season', 'episode']
        filters = ['www.torrenting.com - ']
        for item in os.listdir(directory):
            parsed = PTN.parse(item)

            # get rid of the useless stuff
            for key in list(parsed):
                if key not in keys:
                    del parsed[key]
                else:
                    for f in filters:
                        if f in str(parsed[key]):
                            parsed[key] = parsed[key].replace(f, '')

            if len(parsed) > 0:
                content[item] = parsed

        return content

    def move_content(self, src, content):
        complete_dir = self.config['transmission']['complete']
        tv_dir = self.config['plex']['libraries']['tv']
        movies_dir = self.config['plex']['libraries']['movies']
        _src = str(complete_dir+src)
        if 'episode' in content:
            dest = tv_dir+str(content['title'])+'/Season '+str(content['season'])+'/Episode '+str(content['episode'])
        else:
            dest = movies_dir+content['title']

        if not os.path.isdir(_src):
            file_path, extension = os.path.splitext(_src)
            dest += extension

        # is this cheating?
        if self.test_mode:
            _src = os.getcwd()+_src
            dest = os.getcwd()+dest

        print _src + ' => ' + dest
        shutil.move(_src, dest)
        return dest

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
        for directory in content.iterkeys():
            print '['+str(content.keys().index(directory))+'] - '+directory

        print '################'
        choice = raw_input('select an item: ')
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

