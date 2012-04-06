from distutils.core import setup
import py2exe

files = [('', ['freakingidiot.wav', 'config.json'])]

setup(console=['badger.py'],
    data_files = files)