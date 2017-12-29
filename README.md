# hockeybox
Alternative command script for The HockeyBox

* To use, edit /etc/rc.local on your HockeyBox and point it to the new hockeybox.py script.
* No other changes should be required to the HockeyBox itself.

# CHANGELOG
## hockeybox.py Changes
* Renamed script to hockeybox.py
* HockeyBox will now play any random mp3 from the specified directory, removing the limit on songs. Also removes the numerical naming requirements.
* Improved python code to use more control structures and reduce hard-coding limitations.

## HockeyBox/RPi Changes
* Edit /etc/rc.local to point to new hockeybox.py
* Disabled GUI mode since we don't need it.
* Edited /etc/fstab to mount SETTINGS and HOCKEYBOX since desktop won't automount anymore with GUI disabled.

## HOCKEYBOX USB Drive
* Replaced all MP3 files with legally purchased MP3s.
* Renamed dirs to avoid spaces and capitalization:
    * goal
    * warmup
    * btw
    * intermission
    * penalty
    * powerplay
    * usanthem
    * cdnanthem

# TODO
## Handle Input
* Currently spins in loop polling for input changes, consumes entire CPU
    * Can we sit idle and be notified for change instead?
