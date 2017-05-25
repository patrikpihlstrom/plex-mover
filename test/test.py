#!/usr/bin/python

import sys
import os
import unittest
import json
import shutil
import time
import daemon
from multiprocessing import Process

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(here+'/../plex_mover/')
import plex_mover

class TestPlexMover(unittest.TestCase):
    test = None
    plex_mover = None

    def __init__(self, function, test):
        super(TestPlexMover, self).__init__(function)
        self.plex_mover = plex_mover.PlexMover(test_mode = True)
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
            self.assertIn(item, content.values())

    def test_move_content(self):
        libraries = self.plex_mover.config['plex']['libraries']
        content = self.plex_mover.get_content_in_directory(here+self.plex_mover.config['transmission']['complete'])

        for directory, item in content.iteritems():
            if 'episode' in item:
                self.assertFalse(os.path.exists(os.getcwd()+str(libraries['tv'])+str(item['title'])+'/Season '+str(item['season'])+'/'+directory))
                dirs = self.plex_mover.move_content(directory, item)
                self.assertTrue(os.path.exists(dirs[1]))
            else:
                self.assertFalse(os.path.exists(os.getcwd()+str(libraries['movies'])+directory))
                dirs = self.plex_mover.move_content(directory, item)
                self.assertTrue(os.path.exists(dirs[1]))

class TestPlexMoverDaemon(unittest.TestCase):
    test = None
    plex_mover = None
    libraries = None
    complete = None
    incomplete = None
    process = None

    def __init__(self, function, test):
        super(TestPlexMoverDaemon, self).__init__(function)

        self.test = test
        self.daemon = plex_mover.PlexMoverDaemon(test_mode = True)
        self.plex_mover = self.daemon.plex_mover
        self.libraries = self.plex_mover.config['plex']['libraries']
        self.complete = self.plex_mover.config['transmission']['complete']
        self.incomplete = self.plex_mover.config['transmission']['incomplete']
        self.process = Process(target=self.daemon.run)
        self.process.daemon = True
        self.process.start()
        print "PID: " + str(self.process.pid)

    def setUp(self):
        # plex lib dirs
        if not os.path.exists(here+self.libraries['movies']):
            os.makedirs(here+self.libraries['movies'])
        if not os.path.exists(here+self.libraries['tv']):
            os.makedirs(here+self.libraries['tv'])

        # transmission complete dir
        if not os.path.exists(here+self.complete):
            os.makedirs(here+self.complete)
        if not os.path.exists(here+self.incomplete):
            os.makedirs(here+self.incomplete)

    def tearDown(self):
        libraries = self.plex_mover.config['plex']['libraries']
        complete = self.plex_mover.config['transmission']['complete']
        incomplete = self.plex_mover.config['transmission']['incomplete']
        shutil.rmtree(here+self.libraries['movies'])
        shutil.rmtree(here+self.libraries['tv'])
        shutil.rmtree(here+self.complete)
        shutil.rmtree(here+self.incomplete)

    def test_observe_directory(self):
        # test dirs
        for index, directory in enumerate(self.test['dirs']):
            os.makedirs(here+self.incomplete+directory)
            self.plex_mover.get_content_in_directory(here+self.incomplete)
            paths = self.plex_mover.get_source_destination(directory, self.test['expected_content'][index])
            self.assertFalse(os.path.exists(here+self.complete+directory))
            os.makedirs(here+self.complete+directory)
            time.sleep(0.25)
            self.assertFalse(os.path.exists(here+self.complete+directory))
            self.assertTrue(os.path.exists(paths[1]))

        self.process.terminate()

if __name__ == '__main__':
    config = None
    with open(here+'/dummy_config.json') as config:
        config = json.load(config)

    suite = unittest.TestSuite()
    daemon_suite = unittest.TestSuite()
    for test in config['tests']:
        if 'daemon' in test and test['daemon'] == True:
            daemon_suite.addTest(TestPlexMoverDaemon('test_observe_directory', test))
            unittest.TextTestRunner().run(daemon_suite)
        else:
            suite.addTest(TestPlexMover('test_get_content_in_directory', test))
            unittest.TextTestRunner().run(suite)
            suite.addTest(TestPlexMover('test_move_content', test))
            unittest.TextTestRunner().run(suite)

