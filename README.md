# hockeybox
Alternative command script for The HockeyBox

* Don Seiler, don@seiler.us
    * based on HockeyBox3.py by Greg Manley

## Requirements
### Media Drive
USB drive must be mounted at `/media/hockeybox` with the following subdirectories:

* btw
* goal
* intermission
* penalty
* powerplay
* usanthem

There is no necessary naming format for the mp3 files, other than they must have the `.mp3` filename extension and not begin with a dot (`.`).

### python3
This should be installed standard now, but just in case it isn't, be sure it is.

### vlc
You will need the `vlc` python3 module.

- On a debian-based system you can run `sudo apt-get install python3-vlc`.
- If you prefer `pip` you can run `sudo pip install python-vlc`.

## Use
To have Hockeybox run automatically on startup, we create a systemd service for it.

### Create the file `/etc/systemd/system/hockeybox.service`
```
sudo vi /etc/systemd/system/hockeybox.service
```

### Define the service by writing this to the file (be sure to update the path to the hockeybox.py file)
```
[Unit]
Description=HockeyBox
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /path/to/hockeybox/hockeybox.py

[Install]
WantedBy=multi-user.target
```

### Reload systemd and enable the new service
```
sudo systemctl daemon-reload
sudo systemctl enable hockeybox
```

### Test
You can start the service as a quick test that it is working properly
```
sudo systemctl start hockeybox
```

### Reboot
Finally, reboot your device and confirm that the service starts automatically.