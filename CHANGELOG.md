# hockeybox
Alternative command script for The HockeyBox

* Don Seiler, don@seiler.us
    * based on HockeyBox3.py by Greg Manley

## CHANGELOG

### 202504.1 (XX Apr 2025)
#### hockeybox.py Changes
* Replaced RPi.GPIO with gpiozero library.
* Fixed bug to prevent simultaneous playback of INTERMISSION and any non-INTERMISSION player.

### 202308.1 (20 Aug 2023)
#### hockeybox.py Changes
* Updated for python3
* Changed media directory location to `/media/hockeybox`

### 201811.1 (29 Nov 2018)
#### hockeybox.py Changes
* Added playlist feature for INTERMISSION. Hitting INTERMISSION will generate a random playlist of INTERMISSION songs, same size as the `INTERMISSION_REPEAT_THRESHOLD` (default 5). This allows the operator to leave the Hockeybox unattended for longer intermissions and hit the restroom or concession stand.
* Adding no-repeat thresholds for goals, powerplay and penalty music.

### 201801.1 (9 Jan 2018)
#### hockeybox.py Changes
* Script cleanup, encapsulated light-change logic in functions.
* Using RPi.GPIO's event detection and callback API rather than constantly polling all the inputs.
* Keep small queue of recently played songs for BTW and Intermission to avoid recent repeats.

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
