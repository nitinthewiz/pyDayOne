pyDayOne
========

A Windows based python app to show your Day One entries and let you make new ones. Tested in Windows 7.


FAQ
===

**Q.** Why?

**Ans.** Because Windows Day One support is sad (read: non-existant).

**Q.** Hasn't this been done before on BitBucket

**Ans.** Yes and No. The bitbucket one is in .NET. Very sucky. Python is cross-platform and has everything you need.

**Q.** Bugs exist

**Ans.** Yes they do.


How to Run this?
================

1. You can run it from command prompt/terminal with the command - "python pyDayOne.py"
2. You can compile it into an exe if you have the [cx_freeze library](http://cx-freeze.sourceforge.net/) installed.

   Use the command `python setup.py build` from the directory containing setup.py, and you'll get a `build` directory containing a target-specific directory (such as `exe.win32-2.7`, indicating a Python 2.7 based Win32 executable) containing the pyDayOne executable and the necessary supporting files.

   Use the comamnd `python setup.py bdist_msi` instead, and you'll get a directory called `dist` containing a Windows MSI installer.

Requirements
============

The following python modules need to be installed -

1. wxPython


Major Bugs -
============

1. Doesn't support many languages like Chinese (utf-8 encoding only)
