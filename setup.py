import os
import codecs
from setuptools import setup

readme_path = os.path.join(os.path.dirname(__file__), 'README.md')

with codecs.open(readme_path, mode='r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='plex-mover',
    version='1.0',
    url='https://github.com/patrikpihlstrom/plex-mover',
    description='Extract media information from torrent-like filename',
    packages=['plex_mover'],
    package_data={
        '': ['config.json']
    }
)
