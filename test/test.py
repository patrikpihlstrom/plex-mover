#!/usr/bin/python

import sys
import os
import unittest
import json
import shutil

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here+'/../')
import plex_mover


class TestPlexMover(unittest.TestCase):
    test = None
    plex_mover = None

    def __init__(self, function, test):
        super(TestPlexMover, self).__init__(function)
        self.plex_mover = plex_mover.PlexMover(test_mode=True)
        self.test = test

    def setUp(self):
        libraries = self.plex_mover.config['plex']['libraries']
        complete = self.plex_mover.config['transmission']['complete']

        # plex lib dirs
        if not os.path.exists(here+libraries['movies']):
            os.makedirs(here+libraries['movies'])
        if not os.path.exists(here+libraries['tv']):
            os.makedirs(here+libraries['tv'])

        # transmission complete dir
        if not os.path.exists(here+complete):
            os.makedirs(here+complete)

        # test dirs
        for directory in self.test['dirs']:
            if not os.path.exists(here+complete+directory):
                os.makedirs(here+complete+directory)

    def tearDown(self):
        libraries = self.plex_mover.config['plex']['libraries']
        complete = self.plex_mover.config['transmission']['complete']
        shutil.rmtree(here+libraries['movies'])
        shutil.rmtree(here+libraries['tv'])
        shutil.rmtree(here+complete)

    def test_get_content_in_directory(self):
        content = self.test['content']
        self.assertItemsEqual(self.plex_mover.get_content_in_directory(
            here+self.plex_mover.config['transmission']['complete']), content)

if __name__ == '__main__':
    config = None
    with open(here+'/config.json') as config:
        config = json.load(config)

    suite = unittest.TestSuite()
    for test in config['tests']:
        suite.addTest(TestPlexMover('test_get_content_in_directory', test))

    unittest.TextTestRunner().run(suite)

