from distutils.core import setup
import py2exe

files = [('', ['freakingidiot.wav', 'config.json', 'badger.png'])]

setup(windows=['badger.pyw'],
    data_files = files,
    options = {
    "py2exe": {"dll_excludes": ["MSVCP90.dll"]}
    })