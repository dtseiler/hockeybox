#!/usr/bin/python

# HockeyBox
# by Don Seiler, don@seiler.us
# Based on HockeyBox3.py by Greg Manley
#
# Use 4-space tabs for indentation.

HOCKEYBOX_VERSION = "201712.1"

import RPi.GPIO as GPIO
from time import sleep
import os, random, vlc

print "HockeyBox %s" % HOCKEYBOX_VERSION
print "by Don Seiler, don@seiler.us"
print "Based on HockeyBox3.py (2016) by Greg Manley"

BASE_MP3_DIR = "/media/pi/HOCKEYBOX"
GOAL_MP3_DIR = BASE_MP3_DIR + "/goal"
WARMUP_MP3_DIR = BASE_MP3_DIR + "/warmup"
BTW_MP3_DIR = BASE_MP3_DIR + "/btw"
INTERMISSION_MP3_DIR = BASE_MP3_DIR + "/intermission"
PENALTY_MP3_DIR = BASE_MP3_DIR + "/penalty"
POWERPLAY_MP3_DIR = BASE_MP3_DIR + "/powerplay"
USANTHEM_MP3_DIR = BASE_MP3_DIR + "/usanthem"
CDNANTHEM_MP3_DIR = BASE_MP3_DIR + "/cdnanthem"

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

# Define our VLC object
instance = vlc.Instance()
player = instance.media_player_new()


# Handle button light changes after a button is pushed
def change_lights_after_input(p_output):
    # Turn all button lights off
    GPIO.output(outputs, GPIO.HIGH)
    sleep(0.2)

    # Turn on the STOP light and button that was pressed
    GPIO.output(OUTPUT_STOP, GPIO.LOW)
    GPIO.output(p_output, GPIO.LOW)


# Method for picking random MP3 from specified directory and playing it
# with the VLC player instance.
def play_random_song(mp3_dir):
    # Loop here until file is .mp3 and not a dotfile
    while True:
        song = random.choice(os.listdir(mp3_dir))
        if song.endswith(".mp3") and not song.startswith("."):
            break

    song_path = mp3_dir + "/" + song
    print "Playing %s" % song_path
    song_media = instance.media_new(song_path)
    player.set_media(song_media)
    player.play()


# XXX Why?        
print "Sleeping for 1 second for some reason"
sleep(1.0)

# Flicker the lights
for output in outputs:
    # GPIO.HIGH turns the button lights off
    GPIO.output(output, GPIO.HIGH)
    sleep(0.1)
for output in outputs:
    # GPIO.LOW turns the button lights on
    GPIO.output(output, GPIO.LOW)
    sleep(0.1)
GPIO.output(OUTPUT_STOP, GPIO.HIGH)

print "HockeyBox ready, waiting for input."
# Begin main loop, polling for input
while True:
    # GOAL
    if GPIO.input(INPUT_GOAL):
        print "GOAL"
        change_lights_after_input(OUTPUT_GOAL)

        # DTS:
        # XXX Can we put this outside the loop? Special case if INPUT_STOP
        # Right now it waits here in this block until the the stop riser, 
	    # then the INPUT_STOP is handled at the end
        # Can we try using event_detected() instead of wait_for_edge()?
        play_random_song(GOAL_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # WARM UP
    if GPIO.input(INPUT_WARMUP):
        print "WARMUP"
        change_lights_after_input(OUTPUT_WARMUP)
        play_random_song(WARMUP_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # US Anthem
    if GPIO.input(INPUT_USANTHEM):
        print "US ANTHEM"
        change_lights_after_input(OUTPUT_USANTHEM)
        play_random_song(USANTHEM_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)
        
    # Canadian Anthem
    if GPIO.input(INPUT_CDNANTHEM):
        print "CDN ANTHEM"
        change_lights_after_input(OUTPUT_CDNANTHEM)
        play_random_song(CDNANTHEM_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # Penalty
    if GPIO.input(INPUT_PENALTY):
        print "PENALTY"
        change_lights_after_input(OUTPUT_PENALTY)
        play_random_song(PENALTY_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # Power Play
    if GPIO.input(INPUT_POWERPLAY):
        print "POWERPLAY"
        change_lights_after_input(OUTPUT_POWERPLAY)
        play_random_song(POWERPLAY_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # Intermission
    if GPIO.input(INPUT_INTERMISSION):
        print "INTERMISSION"
        change_lights_after_input(OUTPUT_INTERMISSION)
        play_random_song(INTERMISSION_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # BTW (Between the Whistle)
    if GPIO.input(INPUT_BTW):
        print "BTW"
        change_lights_after_input(OUTPUT_BTW)
        play_random_song(BTW_MP3_DIR)
        GPIO.wait_for_edge(INPUT_STOP, GPIO.RISING)

    # STOP
    if GPIO.input(INPUT_STOP):
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

# This will likely never be called, but good practice
GPIO.cleanup()
