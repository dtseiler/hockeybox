#!/usr/bin/python3

# HockeyBox
# by Don Seiler, don@seiler.us
# Based on HockeyBox3.py by Greg Manley
#
# Use 4-space tabs for indentation
# vim :set ts=4 sw=4 sts=4 et:

HOCKEYBOX_VERSION = "202504.1"

from gpiozero import ButtonBoard, LEDBoard, pi_info
from time import sleep
import os, random, vlc
from signal import pause
from collections import deque
from pkg_resources import require

pi = pi_info()

print("--------------------------------------------")
print("HockeyBox %s" % HOCKEYBOX_VERSION)
print("by Don Seiler, don@seiler.us")
print("Based on HockeyBox3.py (2016) by Greg Manley")
print("--------------------------------------------")
print("Raspberry Pi Model " + pi.model)
print("gpiozero " + require('gpiozero')[0].version)
print("--------------------------------------------")

# Set thresholds for songs played before a song can be re-played
BTW_REPEAT_THRESHOLD = 50
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

# Setup buttons
BUTTON_WARMUP_PIN = 25
BUTTON_BTW_PIN = 21
BUTTON_INTERMISSION_PIN = 12
BUTTON_GOAL_PIN = 20
BUTTON_PENALTY_PIN = 23
BUTTON_POWERPLAY_PIN = 16
BUTTON_USANTHEM_PIN = 7
BUTTON_CDNANTHEM_PIN = 8
BUTTON_STOP_PIN = 24
buttons = ButtonBoard(
    warmup = BUTTON_WARMUP_PIN,
    btw = BUTTON_BTW_PIN,
    intermission = BUTTON_INTERMISSION_PIN,
    goal = BUTTON_GOAL_PIN,
    penalty = BUTTON_PENALTY_PIN,
    powerplay = BUTTON_POWERPLAY_PIN,
    usanthem = BUTTON_USANTHEM_PIN,
    cdnanthem = BUTTON_CDNANTHEM_PIN,
    stop = BUTTON_STOP_PIN,
    bounce_time = 0.05
)

# Setup LEDS
LED_WARMUP_PIN = 27
LED_BTW_PIN = 26
LED_INTERMISSION_PIN = 22
LED_GOAL_PIN = 17
LED_PENALTY_PIN = 19
LED_POWERPLAY_PIN = 6
LED_USANTHEM_PIN = 5
LED_CDNANTHEM_PIN = 4
LED_STOP_PIN = 13
leds = LEDBoard(
    warmup = LED_WARMUP_PIN,
    btw = LED_BTW_PIN,
    intermission = LED_INTERMISSION_PIN,
    goal = LED_GOAL_PIN,
    penalty = LED_PENALTY_PIN,
    powerplay = LED_POWERPLAY_PIN,
    usanthem = LED_USANTHEM_PIN,
    cdnanthem = LED_CDNANTHEM_PIN,
    stop = LED_STOP_PIN,
    _order=('warmup','btw','intermission','goal','penalty','powerplay','usanthem','cdnanthem','stop')
)


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
# cycle_lights_and_on
# Turns all lights off and then on in a flowing sequence
#
def cycle_lights_and_on():
    leds.off()
    for led in leds:
        led.on()
        sleep(0.05)
    leds.stop.off()


#
# change_lights_after_input
# Handle button light changes after a button is pushed
#
def change_lights_after_input(p_led):
    # Turn all button lights off
    leds.off()
    sleep(0.2)

    # Turn on the STOP light and button that was pressed
    leds.stop.on()
    p_led.on()

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
def play_goal():
    print("GOAL")
    change_lights_after_input(leds.goal)
    new_song = ""
    while True:
        new_song = pick_random_song(GOAL_MP3_DIR)
        if new_song in goal_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            goal_played_songs.append(new_song)
            break

    # Keep list at GOAL_REPEAT_THRESHOLD
    if len(goal_played_songs) > GOAL_REPEAT_THRESHOLD:
        print("Removing %s from goal_played_songs list" % goal_played_songs[0])
        goal_played_songs.popleft()
    play_song(new_song)

#
# WARM-UP
#
def play_warmup():
    print("WARMUP")
    change_lights_after_input(leds.warmup)
    play_song(pick_random_song(WARMUP_MP3_DIR))

#
# US ANTHEM
#
def play_usanthem():
    print("USANTHEM")
    change_lights_after_input(leds.usanthem)
    play_song(pick_random_song(USANTHEM_MP3_DIR))

#
# CDN ANTHEM
#
def play_cdnanthem():
    print("CDNANTHEM")
    change_lights_after_input(leds.cdnanthem)
    play_song(pick_random_song(CDNANTHEM_MP3_DIR))

#
# PENALTY
#
def play_penalty():
    print("PENALTY")
    change_lights_after_input(leds.penalty)
    new_song = ""
    while True:
        new_song = pick_random_song(PENALTY_MP3_DIR)
        if new_song in penalty_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            penalty_played_songs.append(new_song)
            break

    # Keep list at PENALTY_REPEAT_THRESHOLD
    if len(penalty_played_songs) > PENALTY_REPEAT_THRESHOLD:
        print("Removing %s from penalty_played_songs list" % penalty_played_songs[0])
        penalty_played_songs.popleft()
    play_song(new_song)

#
# POWERPLAY
#
def play_powerplay():
    print("POWERPLAY")
    change_lights_after_input(leds.powerplay)
    new_song = ""
    while True:
        new_song = pick_random_song(POWERPLAY_MP3_DIR)
        if new_song in powerplay_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            powerplay_played_songs.append(new_song)
            break

    # Keep list at POWERPLAY_REPEAT_THRESHOLD
    if len(powerplay_played_songs) > POWERPLAY_REPEAT_THRESHOLD:
        print("Removing %s from powerplay_played_songs list" % powerplay_played_songs[0])
        powerplay_played_songs.popleft()
    play_song(new_song)

#
# INTERMISSION
#
def play_intermission():
    print("INTERMISSION")
    change_lights_after_input(leds.intermission)

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
            break

    list_player.set_media_list(intermission_playlist)
    list_player.play()


#
# BTW
#
def play_btw():
    print("BTW")
    change_lights_after_input(leds.btw)
    new_song = ""
    while True:
        new_song = pick_random_song(BTW_MP3_DIR)
        if new_song in btw_played_songs:
            print("Song %s has already been played, skipping." % new_song)
        else:
            btw_played_songs.append(new_song)
            break

    # Keep list at BTW_REPEAT_THRESHOLD
    if len(btw_played_songs) > BTW_REPEAT_THRESHOLD:
        print("Removing %s from btw_played_songs list" % btw_played_songs[0])
        btw_played_songs.popleft()
    play_song(new_song)

#
# STOP
#
def stop_playback():
    print("STOP")
    sleep(0.3)
    if player.is_playing():
        print("Stopping player")
        player.stop()
    if list_player.is_playing():
        print("Stopping list player")
        list_player.stop()
    print("Music Stopped")
    cycle_lights_and_on()

# Define event detections and their callbacks
buttons.goal.when_pressed = play_goal
buttons.warmup.when_pressed = play_warmup
buttons.usanthem.when_pressed = play_usanthem
buttons.cdnanthem.when_pressed = play_cdnanthem
buttons.penalty.when_pressed = play_penalty
buttons.powerplay.when_pressed = play_powerplay
buttons.intermission.when_pressed = play_intermission
buttons.btw.when_pressed = play_btw
buttons.stop.when_pressed = stop_playback

#
# Event Handlers
#

# Sends the STOP signal when a song has finished playing to completion
def song_finished(event):
    print("Song finished, stopping playback")
    stop_playback()

# Advances to the next song for intermission lists
def intermission_item_played(event):
    global intermission_num_played
    intermission_num_played += 1
    print("Items Played: %d" % intermission_num_played)

player_events.event_attach(vlc.EventType.MediaPlayerEndReached, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerPlayed, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, intermission_item_played)

# Flicker the lights
print("Light 'em up.")
cycle_lights_and_on()

print("***********************************")
print("HockeyBox ready, waiting for input.")
print("***********************************")
# Pause so event handlers can do the rest
pause()