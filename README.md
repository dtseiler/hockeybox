# hockeybox
Alternative command script for The HockeyBox
by Don Seiler, don@seiler.us
Based on HockeyBox3.py by Greg Manley


## USE
* To use, edit /etc/rc.local on your HockeyBox and point it to the new hockeybox.py script.
* No other changes should be required to the HockeyBox itself.


## TODO
* Display will show "PulseAudio server connection failure: Connection refused" when the VLC instance is created and when songs are played. It doesn't seem to affect the actual sound as that works fine, but I'd rather not have unexplained errors. Need to find out what is causing this and fix it.
* Why is GPIO.HIGH setting lights off, and LOW setting them on? Sounds like it should be reverse. Is this a pull up/down thing?
* GOAL: Play GH.mp3 separately, then play song from goal dir


## CHANGELOG

### 201801.1 (TBD)
#### hockeybox.py Changes
* Script cleanup, encapsulated light-change logic in functions.
* Using RPi.GPIO's event detection and callback API rather than constantly polling all the inputs.
* Keep small queue of recently played songs for BTW and Intermission to avoid recent repeats.
* For intermission, keep playing random songs until STOP is pressed

#### HOCKEYBOX USB Drive
* Created `goal_horn` directory separate from goal directory, moved GH.mp3 to `goal_horn`
    * This way we can play the horn sound on its own and don't require users to splice it into their goal songs.

### 201712.1 (27 Dec 2017)
#### hockeybox.py Changes
* Renamed script to hockeybox.py
* HockeyBox will now play any random mp3 from the specified directory, removing the limit on songs. Also removes the numerical naming requirements.
* Improved python code to use more control structures and remove hard-coding limitations.

#### HockeyBox/RPi Changes
* Edit /etc/rc.local to point to new hockeybox.py
* Disabled GUI mode since we don't need it.
* Edited /etc/fstab to mount SETTINGS and HOCKEYBOX since desktop won't automount anymore with GUI disabled.

#### HOCKEYBOX USB Drive
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
