## Overview

A tool to help restore files from an iTunes backup of an iPhone or iPad.

## How-to

For now - edit the `main.py` file and fill out the settings on the top, including the path to your backup folder.

## TODO
Arranged by rough priority
### Fixes

* Verify "plist timestamp recovery"
* Improve plist handling code (don't just use a magic string & raw handling of bytes-to-date)
* Fix (or remove) EXIF-based timestamp option

### Features

* Use arguments/parameters rather than "edit my variables"
* Symbolic-link based "recovery" tree building
  * Can be implemented cross-platform using `os.symlink`
* GUI?
