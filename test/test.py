#!/usr/bin/python

import sys
import os
import unittest
import json
import shutil

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here+'/../plex_mover/')
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
        expected_content = self.test['expected_content']
        content = self.plex_mover.get_content_in_directory(here+self.plex_mover.config['transmission']['complete'])

        for item in expected_content:
            print(str(item) + ' ## ' + str(content.values()))
            print('#####################################')
            self.assertIn(item, content.values())

    def test_move_content(self):
        libraries = self.plex_mover.config['plex']['libraries']
        content = self.plex_mover.get_content_in_directory(here+self.plex_mover.config['transmission']['complete'])

        for directory, item in content.iteritems():
            if 'episode' in item:
                self.assertFalse(os.path.exists(os.getcwd()+str(libraries['tv'])+str(item['title'])+'/Season '+str(item['season'])+'/'+directory))
                dest = self.plex_mover.move_content(directory, item)
                self.assertTrue(os.path.exists(dest))
            else:
                self.assertFalse(os.path.exists(os.getcwd()+str(libraries['movies'])+directory))
                dest = self.plex_mover.move_content(directory, item)
                self.assertTrue(os.path.exists(dest))

if __name__ == '__main__':
    config = None
    with open(here+'/dummy_config.json') as config:
        config = json.load(config)

    suite = unittest.TestSuite()
    for test in config['tests']:
        suite.addTest(TestPlexMover('test_get_content_in_directory', test))
        suite.addTest(TestPlexMover('test_move_content', test))

    unittest.TextTestRunner().run(suite)

