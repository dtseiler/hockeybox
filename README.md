# hockeybox
Alternative command script for The HockeyBox

* Don Seiler, don@seiler.us
    * based on HockeyBox3.py by Greg Manley

## Requirements
USB drive must be mounted at `/media/pi/HOCKEYBOX` with the following subdirectories:

* btw
* cdnanthem
* goal
* intermission
* penalty
* powerplay
* usanthem
* warmup

There is no necessary naming format for the mp3 files, other than they must have the `.mp3` filename extension and not begin with a dot (`.`).

## Use
1. Edit /etc/rc.local on your HockeyBox and point it to the new hockeybox.py script.
2. Restart HockeyBox, it should run hockeybox.py automatically.

