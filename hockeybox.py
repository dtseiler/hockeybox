#!/usr/bin/python

# HockeyBox
# by Don Seiler, don@seiler.us
# Based on HockeyBox3.py by Greg Manley
#
# Use 4-space tabs for indentation.

HOCKEYBOX_VERSION = "201801.1"

import RPi.GPIO as GPIO
from time import sleep
import os, random, vlc
from collections import deque

print "--------------------------------------------"
print "HockeyBox %s" % HOCKEYBOX_VERSION
print "by Don Seiler, don@seiler.us"
print "Based on HockeyBox3.py (2016) by Greg Manley"
print "--------------------------------------------"
print "RPI %s" % GPIO.RPI_INFO
print "RPi.GPIO %s" % GPIO.VERSION
print "--------------------------------------------"

BASE_MP3_DIR = "/media/pi/HOCKEYBOX"
GOAL_MP3_DIR = BASE_MP3_DIR + "/goal"
WARMUP_MP3_DIR = BASE_MP3_DIR + "/warmup"
BTW_MP3_DIR = BASE_MP3_DIR + "/btw"
INTERMISSION_MP3_DIR = BASE_MP3_DIR + "/intermission"
PENALTY_MP3_DIR = BASE_MP3_DIR + "/penalty"
POWERPLAY_MP3_DIR = BASE_MP3_DIR + "/powerplay"
USANTHEM_MP3_DIR = BASE_MP3_DIR + "/usanthem"
CDNANTHEM_MP3_DIR = BASE_MP3_DIR + "/cdnanthem"

# Track which songs have been played
btw_played_songs = deque([])
BTW_REPEAT_THRESHOLD = 10
intermission_played_songs = deque([])
INTERMISSION_REPEAT_THRESHOLD = 3

#
# GPIO Setup
#

# Set GPIO to BCM mode
GPIO.setmode (GPIO.BCM)
inputs = []
outputs = []

# Setup input channels
INPUT_WARMUP=25
inputs.append(INPUT_WARMUP)
INPUT_BTW=21
inputs.append(INPUT_BTW)
INPUT_INTERMISSION=12
inputs.append(INPUT_INTERMISSION)
INPUT_GOAL=20
inputs.append(INPUT_GOAL)
INPUT_PENALTY=23
inputs.append(INPUT_PENALTY)
INPUT_POWERPLAY=16
inputs.append(INPUT_POWERPLAY)
INPUT_USANTHEM=7
inputs.append(INPUT_USANTHEM)
INPUT_CDNANTHEM=8
inputs.append(INPUT_CDNANTHEM)
INPUT_STOP=24
inputs.append(INPUT_STOP)
GPIO.setup(inputs, GPIO.IN)

# Setup output channels
OUTPUT_WARMUP=27
outputs.append(OUTPUT_WARMUP)
OUTPUT_BTW=26
outputs.append(OUTPUT_BTW)
OUTPUT_INTERMISSION=22
outputs.append(OUTPUT_INTERMISSION)
OUTPUT_GOAL=17
outputs.append(OUTPUT_GOAL)
OUTPUT_PENALTY=19
outputs.append(OUTPUT_PENALTY)
OUTPUT_POWERPLAY=6
outputs.append(OUTPUT_POWERPLAY)
OUTPUT_USANTHEM=5
outputs.append(OUTPUT_USANTHEM)
OUTPUT_CDNANTHEM=4
outputs.append(OUTPUT_CDNANTHEM)
OUTPUT_STOP=13
outputs.append(OUTPUT_STOP)
GPIO.setup(outputs, GPIO.OUT)


#
# VLC Player Setup
#

# Define our VLC object
instance = vlc.Instance()
player = instance.media_player_new()


#
# Function Definitions
#

#
# change_lights_after_input
# Handle button light changes after a button is pushed
#
def change_lights_after_input(p_output):
    # Turn all button lights off
    GPIO.output(outputs, GPIO.HIGH)
    sleep(0.2)

    # Turn on the STOP light and button that was pressed
    GPIO.output(OUTPUT_STOP, GPIO.LOW)
    GPIO.output(p_output, GPIO.LOW)

#
# pick_random_song
# Picking random MP3 from specified directory and play it
#   with the VLC player instance.
#
def pick_random_song(p_mp3_dir):
    # Loop here until file is .mp3 and not a dotfile
    while True:
        song = random.choice(os.listdir(p_mp3_dir))
        if song.endswith(".mp3") and not song.startswith("."):

            break
    song_path = p_mp3_dir + "/" + song
    return song_path

def play_song(p_song):
    # XXX Should we call player.stop() here first?
    player.stop()
    print "Playing %s" % p_song
    song_media = instance.media_new(p_song)
    player.set_media(song_media)
    player.play()

#
# GOAL
#
def play_goal(channel):
    print "GOAL"
    change_lights_after_input(OUTPUT_GOAL)
    play_song(pick_random_song(GOAL_MP3_DIR))

#
# WARM-UP
#
def play_warmup(channel):
    print "WARMUP"
    change_lights_after_input(OUTPUT_WARMUP)
    play_song(pick_random_song(WARMUP_MP3_DIR))

#
# US ANTHEM
#
def play_usanthem(channel):
    print "USANTHEM"
    change_lights_after_input(OUTPUT_USANTHEM)
    play_song(pick_random_song(USANTHEM_MP3_DIR))

#
# CDN ANTHEM
#
def play_cdnanthem(channel):
    print "CDNANTHEM"
    change_lights_after_input(OUTPUT_CDNANTHEM)
    play_song(pick_random_song(CDNANTHEM_MP3_DIR))

#
# PENALTY
#
def play_penalty(channel):
    print "PENALTY"
    change_lights_after_input(OUTPUT_PENALTY)
    play_song(pick_random_song(PENALTY_MP3_DIR))

#
# POWERPLAY
#
def play_powerplay(channel):
    print "POWERPLAY"
    change_lights_after_input(OUTPUT_POWERPLAY)
    play_song(pick_random_song(POWERPLAY_MP3_DIR))

#
# INTERMISSION
#
def play_intermission(channel):
    print "INTERMISSION"
    change_lights_after_input(OUTPUT_INTERMISSION)
    new_song = ""
    while True:
        new_song = pick_random_song(INTERMISSION_MP3_DIR)
        if new_song in intermission_played_songs:
            print "Song %s has already been played, skipping." % new_song
        else:
            print "Playing song %s" % new_song
            intermission_played_songs.append(new_song)
            break;

    # Keep list at INTERMISSION_REPEAT_THRESHOLD
    if len(intermission_played_songs) > INTERMISSION_REPEAT_THRESHOLD:
        print "Removing %s from intermission_played_songs list" % intermission_played_songs[0]
        intermission_played_songs.popleft()
    play_song(new_song)

#
# BTW
#
def play_btw(channel):
    print "BTW"
    change_lights_after_input(OUTPUT_BTW)
    new_song = ""
    while True:
        new_song = pick_random_song(BTW_MP3_DIR)
        if new_song in btw_played_songs:
            print "Song %s has already been played, skipping." % new_song
        else:
            print "Playing song %s" % new_song
            btw_played_songs.append(new_song)
            break;

    # Keep list at BTW_REPEAT_THRESHOLD
    if len(btw_played_songs) > BTW_REPEAT_THRESHOLD:
        print "Removing %s from btw_played_songs list" % btw_played_songs[0]
        btw_played_songs.popleft()
    play_song(new_song)

#
# STOP
#
def stop_playback(channel):
    print "STOP"
    sleep(0.3)
    player.stop()
    GPIO.output(outputs, GPIO.HIGH)
    print "Music Stopped"
    for output in outputs:
        # GPIO.LOW turns the button lights on
        GPIO.output(output, GPIO.LOW)
        sleep(0.05)
    GPIO.output(OUTPUT_STOP, GPIO.HIGH)

# Define event detections and their callbacks
GPIO.add_event_detect(INPUT_GOAL, GPIO.RISING, callback=play_goal, bouncetime=1000)
GPIO.add_event_detect(INPUT_WARMUP, GPIO.RISING, callback=play_warmup, bouncetime=1000)
GPIO.add_event_detect(INPUT_USANTHEM, GPIO.RISING, callback=play_usanthem, bouncetime=1000)
GPIO.add_event_detect(INPUT_CDNANTHEM, GPIO.RISING, callback=play_cdnanthem, bouncetime=1000)
GPIO.add_event_detect(INPUT_PENALTY, GPIO.RISING, callback=play_penalty, bouncetime=1000)
GPIO.add_event_detect(INPUT_POWERPLAY, GPIO.RISING, callback=play_powerplay, bouncetime=1000)
GPIO.add_event_detect(INPUT_INTERMISSION, GPIO.RISING, callback=play_intermission, bouncetime=1000)
GPIO.add_event_detect(INPUT_BTW, GPIO.RISING, callback=play_btw, bouncetime=1000)
GPIO.add_event_detect(INPUT_STOP, GPIO.RISING, callback=stop_playback, bouncetime=1000)

# Flicker the lights
print "Light 'em up."
for output in outputs:
    # GPIO.HIGH turns the button lights off
    GPIO.output(output, GPIO.HIGH)
    sleep(0.1)
for output in outputs:
    # GPIO.LOW turns the button lights on
    GPIO.output(output, GPIO.LOW)
    sleep(0.1)
GPIO.output(OUTPUT_STOP, GPIO.HIGH)

print "***********************************"
print "HockeyBox ready, waiting for input."
print "***********************************"
# Begin main loop, polling for input
while True:
    # Event detection should be running during this loop
    sleep(0.02)
    # Wonder if we should put a wait_for_edge on INPUT_STOP in here?

# This will likely never be called, but good practice
GPIO.cleanup()
