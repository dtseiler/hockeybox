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

### python3
This should be installed standard now, but just in case it isn't, be sure it is.

### vlc
You will need the `vlc` python3 module.

- On a debian-based system you can run `sudo apt-get install python3-vlc`.
- If you prefer `pip` you can run `sudo pip install python-vlc`.

## Use
1. Edit /etc/rc.local on your HockeyBox and point it to the new hockeybox.py script.
    - e.g. `/home/foo/hockeybox/hockeybox.py &`
    - Be sure to add this line just before the `exit 0` line at the end of the file.
2. Restart HockeyBox, it should run hockeybox.py automatically.

