=== badger ===
v. 0.31
(c) 2012 Jeff Melville
https://github.com/jeffmelville/badger
dev@jeffmelville.com

See below for licensing

==== About ====
Badger is a tool I wrote to remind me when I leave my smartcard in my laptop.
It provides a configurable set of notifications that are triggered when
a computer is locked with a smartcard still inserted.

=== Requirements ===
badger is currently targeted for Windows only. It relies on Windows API calls
via ctypes to determine when the screen is locked and provide popup alerts.
I have only really tested it with Windows 7 64-bit so far.

Python. Written with 2.7, but others should work.
    -- Uses ctypes, built in as of Python 2.5
pyscard for smart card support (http://pyscard.sourceforge.net/) Tested with 1.6.10
py2exe (only needed to create distributable exe's)

=== Features ===
badger currently supports 3 notification modes:
- SoundHandler: Play a wav file (configurable)
- PopupHandler: Display a popup message over the lock screen
- EmailHandler: Send an email (handy for sending an SMS to a phone)

=== Configuration ===
Configuration is performed using the config.json file in the badger directory
TODO: Add more information about configuration

=== Usage ===
Run badger.pyw.  If you have built an exe (see below), run badger.exe.
It will show up in the system tray. Add a shortcut to your startup folder!

NOTE: Badger dies silently with configuration errors right now. Make sure the tray icon
is there.

=== Making an EXE ===
A build file is included to create a distributable exe file. Run:
python setup.py py2exe
in the top level dir. It will create a "build" folder that can be zipped and distributed.

The exe may have a dependency on MSVCP90.dll, which is not included in the build folder.
See http://www.microsoft.com/download/en/details.aspx?displaylang=en&id=29 for details.
In my experience, a lot of people already have this DLL.

=== Known Issues ===
See issue tracker at https://github.com/jeffmelville/badger for up to date info
- UAC prompts are detected as lock screens and may generate notifications
- There is a race case with the PopupHandler if the popup is generated too close to the screen
  being locked. The configurable "delay" parameter exists as a workaround for now. The 
  value in the default config.json has worked well on my machine

=== License ===
badger is distributed as modified BSD:
# Copyright (c) 2012, Jeff Melville
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the author nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

