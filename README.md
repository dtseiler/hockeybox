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
## Disable GUI
* We can disable GUI via raspi-config
    * However when we do that, the SETTINGS and HOCKEYBOX volumes are not mounted.
    * Need to see if audio works as well.
