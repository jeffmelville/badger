from distutils.core import setup
import py2exe
import sys
sys.path.append("src")

files = [('', ['src/freakingidiot.wav', 'src/config.json', 'src/badger.png'])]

setup(windows=['src/badger.pyw'],
    data_files = files,
    options = {
    "py2exe": {"dll_excludes": ["MSVCP90.dll"]}
    })