#!/usr/bin/python

import sys
import os
import json
import sys
import shutil
import time
from itertools import ifilterfalse
from os.path import expanduser

import PTN
from tvnamer.utils import FileParser, EpisodeInfo, DatedEpisodeInfo, NoSeasonEpisodeInfo
from tvnamer.tvnamer_exceptions import (InvalidPath, InvalidFilename,
ShowNotFound, DataRetrievalError, SeasonNotFound, EpisodeNotFound,
EpisodeNameNotFound, ConfigValueError, UserAbort)

__metaclass__ = type
class PlexMover:
    config = None
    test_mode = False
    fetched_titles = {}

    def __init__(self, test_mode = False):
        self.test_mode = test_mode
        here = os.path.dirname(os.path.abspath(__file__))
        if test_mode == True:
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
        if not os.path.exists(directory):
            return

        content = {}
        keys = ['title', 'season', 'episode']
        for item in os.listdir(directory):
            parsed = PTN.parse(item)

            # get rid of the useless stuff
            for key in list(parsed):
                if key not in keys:
                    del parsed[key]

            if len(parsed) > 0:
                if 'title' in parsed:
                    fetched_title = None

                    try:
                        if 'episode' in parsed:
                            parsed['title'] = parsed['title'].lower()
                            fetched_title = FileParser(parsed['title']+'.S'+str(parsed['season'])+'E'+str(parsed['episode'])).parse().generateFilename()
                        else:
                            fetched_title = FileParser(parsed['title']).parse().generateFilename()
                    except InvalidFilename:
                        fetched_title = parsed['title']

                    if fetched_title != None:
                        if '].' in fetched_title:
                            index = fetched_title.index('].')
                            fetched_title = fetched_title[:index] + ']'

                        self.fetched_titles[parsed['title']] = fetched_title

                    content[item] = parsed

        return content

    def get_source_destination(self, src, content):
        directories ={
            'complete': self.config['transmission']['complete'],
            'tv': self.config['plex']['libraries']['tv'],
            'movies': self.config['plex']['libraries']['movies']
        }

        _src = str(directories['complete']+src)

        if 'episode' in content:
            if content['title'] in self.fetched_titles:
                dest = directories['tv']+content['title']+'/Season '+str(content['season'])+'/'+self.fetched_titles[content['title']]
            else:
                dest = directories['tv']+content['title']+'/Season '+str(content['season'])+'/'+content['title']
        else:
            if content['title'] in self.fetched_titles:
                dest = directories['movies']+self.fetched_titles[content['title']]
            else:
                dest = directories['movies']+content['fetched_title']

        if not os.path.isdir(_src):
            file_path, extension = os.path.splitext(_src)
            dest += extension

        if self.test_mode:
            _src = os.getcwd()+_src
            dest = os.getcwd()+dest

        return (_src, dest)

    def move_content(self, src, content, verbose = False):
        directories = self.get_source_destination(src, content)

        dest = directories[1].rsplit('/', 1)[0]
        if not os.path.exists(dest):
            os.makedirs(dest)

        if verbose:
            print directories[0] + ' => ' + directories[1]

        shutil.move(directories[0], directories[1])
        return directories

class PlexMoverDaemon:
    plex_mover = None
    test_mode = False
    complete = None

    def __init__(self, test_mode = False):
        self.plex_mover = PlexMover(test_mode)
        self.test_mode = test_mode
        self.complete = self.plex_mover.config['transmission']['complete']

        if self.test_mode:
                self.complete = os.getcwd() + self.complete

    def run(self):
        while True:
            if os.path.exists(self.complete):
                content = self.plex_mover.get_content_in_directory(self.complete)
                for key, val in content.iteritems():
                    self.plex_mover.move_content(key, val)
            else:
                print 'transmission complete dir not found'
                return

def main(test_mode = False, daemon = False):
    if daemon:
        plex_mover = PlexMoverDaemon(test_mode)
        plex_mover.run()
    else:
        plex_mover = PlexMover(test_mode)
        complete_dir = plex_mover.config['transmission']['complete']
        content = plex_mover.get_content_in_directory(complete_dir)
        if content == None:
            return

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
                plex_mover.move_content(key, val, True)
        else:
            plex_mover.move_content(choices[choice], content[choices[choice]], True)

if __name__ == '__main__':
    daemon = False
    for x in sys.argv:
        if x in ['-d', '-D', '--daemon']:
            daemon = True

    main(False, daemon)

