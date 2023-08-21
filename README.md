# hockeybox
Alternative command script for The HockeyBox

* Don Seiler, don@seiler.us
    * based on HockeyBox3.py by Greg Manley

## Requirements
### Media Drive
USB drive must be mounted at `/media/hockeybox` with the following subdirectories:

* btw
* cdnanthem
* goal
* intermission
* penalty
* powerplay
* usanthem
* warmup

There is no necessary naming format for the mp3 files, other than they must have the `.mp3` filename extension and not begin with a dot (`.`).

### vlc
You will need the `vlc` python3 module.

- On a debian-based system you can run `sudo apt-get install python3-vlc`.
- If you prefer `pip` you can run `sudo pip install python-vlc`.

## Use
1. Edit /etc/rc.local on your HockeyBox and point it to the new hockeybox.py script.
2. Restart HockeyBox, it should run hockeybox.py automatically.

