from distutils.core import setup
import sys
sys.path.append("src")


files = [('', ['src/freakingidiot.wav', 'src/config.json', 'src/badger.png'])]
if sys.platform=="win32":
    import py2exe
    setup(windows=['src/badger.pyw'],
        data_files = files,
        options = {
        "py2exe": {"dll_excludes": ["MSVCP90.dll"]}
        })
elif sys.platform=="darwin":
    import py2app
    setup(app=['src/badger.pyw'],
        data_files = files)
else:
    print "Installer not supported on this platform"
    exit(1)
