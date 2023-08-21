#!/usr/bin/python3

# HockeyBox
# by Don Seiler, don@seiler.us
# Based on HockeyBox3.py by Greg Manley
#
# Use 4-space tabs for indentation
# vim :set ts=4 sw=4 sts=4 et:

HOCKEYBOX_VERSION = "202308.1"

import RPi.GPIO as GPIO
from time import sleep
import os, random, vlc
from collections import deque

print("--------------------------------------------")
print("HockeyBox %s" % HOCKEYBOX_VERSION)
print("by Don Seiler, don@seiler.us")
print("Based on HockeyBox3.py (2016) by Greg Manley")
print("--------------------------------------------")
print("RPI %s" % GPIO.RPI_INFO)
print("RPi.GPIO %s" % GPIO.VERSION)
print("--------------------------------------------")

# Set thresholds for songs played before a song can be re-played
BTW_REPEAT_THRESHOLD = 25
INTERMISSION_REPEAT_THRESHOLD = 5
GOAL_REPEAT_THRESHOLD = 4
PENALTY_REPEAT_THRESHOLD = 4
POWERPLAY_REPEAT_THRESHOLD = 4

# mp3 locations
BASE_MP3_DIR = "/media/hockeybox"
GOAL_MP3_DIR = BASE_MP3_DIR + "/goal"
WARMUP_MP3_DIR = BASE_MP3_DIR + "/warmup"
BTW_MP3_DIR = BASE_MP3_DIR + "/btw"
INTERMISSION_MP3_DIR = BASE_MP3_DIR + "/intermission"
PENALTY_MP3_DIR = BASE_MP3_DIR + "/penalty"
POWERPLAY_MP3_DIR = BASE_MP3_DIR + "/powerplay"
USANTHEM_MP3_DIR = BASE_MP3_DIR + "/usanthem"
CDNANTHEM_MP3_DIR = BASE_MP3_DIR + "/cdnanthem"

# Queues to track played songs
btw_played_songs = deque([])
intermission_num_played = 0
intermission_played_songs = deque([])
goal_played_songs = deque([])
penalty_played_songs = deque([])
powerplay_played_songs = deque([])

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
player_events = player.event_manager()
list_player = instance.media_list_player_new()
list_events = list_player.event_manager()


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
# Picking random MP3 from specified directory
#
def pick_random_song(p_mp3_dir):
    # Loop here until file is .mp3 and not a dotfile
    while True:
        song = random.choice(os.listdir(p_mp3_dir))
        if song.endswith(".mp3") and not song.startswith("."):
            break

    song_path = p_mp3_dir + "/" + song
    return song_path

#
# play_song
# Play specified song (mp3 file path) through VLC MediaPlayer instance
#
def play_song(p_song):
    # Stop playing if anything is currently playing
    if player.is_playing():
        player.stop()
    print("Playing %s" % p_song)
    player.set_media(instance.media_new(p_song))
    player.play()

#
# GOAL
#
def play_goal(channel):
    print("GOAL")
    change_lights_after_input(OUTPUT_GOAL)
    new_song = ""
    while True:
        new_song = pick_random_song(GOAL_MP3_DIR)
        if new_song in goal_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            goal_played_songs.append(new_song)
            break;

    # Keep list at GOAL_REPEAT_THRESHOLD
    if len(goal_played_songs) > GOAL_REPEAT_THRESHOLD:
        print("Removing %s from goal_played_songs list" % goal_played_songs[0])
        goal_played_songs.popleft()
    play_song(new_song)

#
# WARM-UP
#
def play_warmup(channel):
    print("WARMUP")
    change_lights_after_input(OUTPUT_WARMUP)
    play_song(pick_random_song(WARMUP_MP3_DIR))

#
# US ANTHEM
#
def play_usanthem(channel):
    print("USANTHEM")
    change_lights_after_input(OUTPUT_USANTHEM)
    play_song(pick_random_song(USANTHEM_MP3_DIR))

#
# CDN ANTHEM
#
def play_cdnanthem(channel):
    print("CDNANTHEM")
    change_lights_after_input(OUTPUT_CDNANTHEM)
    play_song(pick_random_song(CDNANTHEM_MP3_DIR))

#
# PENALTY
#
def play_penalty(channel):
    print("PENALTY")
    change_lights_after_input(OUTPUT_PENALTY)
    new_song = ""
    while True:
        new_song = pick_random_song(PENALTY_MP3_DIR)
        if new_song in penalty_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            penalty_played_songs.append(new_song)
            break;

    # Keep list at PENALTY_REPEAT_THRESHOLD
    if len(penalty_played_songs) > PENALTY_REPEAT_THRESHOLD:
        print("Removing %s from penalty_played_songs list" % penalty_played_songs[0])
        penalty_played_songs.popleft()
    play_song(new_song)

#
# POWERPLAY
#
def play_powerplay(channel):
    print("POWERPLAY")
    change_lights_after_input(OUTPUT_POWERPLAY)
    new_song = ""
    while True:
        new_song = pick_random_song(POWERPLAY_MP3_DIR)
        if new_song in powerplay_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            powerplay_played_songs.append(new_song)
            break;

    # Keep list at POWERPLAY_REPEAT_THRESHOLD
    if len(powerplay_played_songs) > POWERPLAY_REPEAT_THRESHOLD:
        print("Removing %s from powerplay_played_songs list" % powerplay_played_songs[0])
        powerplay_played_songs.popleft()
    play_song(new_song)

#
# INTERMISSION
#
def play_intermission(channel):
    print("INTERMISSION")
    change_lights_after_input(OUTPUT_INTERMISSION)

    # If we queue N songs but only play P, we should remove the last N-P songs from the played list 
    global intermission_num_played
    if intermission_num_played > 0:
        reclaim_count = INTERMISSION_REPEAT_THRESHOLD - intermission_num_played
        print("Taking back %d songs from the already-played list." % reclaim_count)
        for i in range(reclaim_count):
            print("Reclaiming %s from intermission_played_songs list" % intermission_played_songs[-1])
            intermission_played_songs.pop()

    # Now remove any others over the threshold
    while len(intermission_played_songs) > INTERMISSION_REPEAT_THRESHOLD:
        print("Removing %s from intermission_played_songs list" % intermission_played_songs[-1])
        intermission_played_songs.pop()

    # Build Song List
    intermission_num_played = 0
    intermission_playlist = instance.media_list_new()

    new_song = ""
    while True:
        new_song = pick_random_song(INTERMISSION_MP3_DIR)
        if new_song in intermission_played_songs:
            print("Song %s has already been added to the playlist, skipping." % new_song)
        else:
            print("Adding song %s to intermission play list." % new_song)
            intermission_played_songs.append(new_song)
            intermission_playlist.add_media(instance.media_new(new_song))

        if intermission_playlist.count() >= INTERMISSION_REPEAT_THRESHOLD:
            break;

    list_player.set_media_list(intermission_playlist)
    list_player.play()


#
# BTW
#
def play_btw(channel):
    print("BTW")
    change_lights_after_input(OUTPUT_BTW)
    new_song = ""
    while True:
        new_song = pick_random_song(BTW_MP3_DIR)
        if new_song in btw_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            btw_played_songs.append(new_song)
            break;

    # Keep list at BTW_REPEAT_THRESHOLD
    if len(btw_played_songs) > BTW_REPEAT_THRESHOLD:
        print("Removing %s from btw_played_songs list" % btw_played_songs[0])
        btw_played_songs.popleft()
    play_song(new_song)

#
# STOP
#
def stop_playback(channel):
    print("STOP")
    sleep(0.3)
    if player.is_playing():
        print("Stopping player")
        player.stop()
    if list_player.is_playing():
        print("Stopping list player")
        list_player.stop()
    GPIO.output(outputs, GPIO.HIGH)
    print("Music Stopped")
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

#
# Event Handlers
#

# Sends the STOP signal when a song has finished playing to completion
def song_finished(event):
    print("Song finished, stopping playback")
    stop_playback(INPUT_STOP)

# Advances to the next song for intermission lists
def intermission_item_played(event):
    global intermission_num_played
    intermission_num_played += 1
    print("Items Played: %d" % intermission_num_played)
    #sleep(1)

player_events.event_attach(vlc.EventType.MediaPlayerEndReached, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerPlayed, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, intermission_item_played)


# Flicker the lights
print("Light 'em up.")
for output in outputs:
    # GPIO.HIGH turns the button lights off
    GPIO.output(output, GPIO.HIGH)
    sleep(0.1)
for output in outputs:
    # GPIO.LOW turns the button lights on
    GPIO.output(output, GPIO.LOW)
    sleep(0.1)
GPIO.output(OUTPUT_STOP, GPIO.HIGH)

print("***********************************")
print("HockeyBox ready, waiting for input.")
print("***********************************")
# Begin main loop, polling for input
while True:
    # Event detection should be running during this loop
    sleep(0.02)
    # Wonder if we should put a wait_for_edge on INPUT_STOP in here?

# This will likely never be called, but good practice
GPIO.cleanup()
