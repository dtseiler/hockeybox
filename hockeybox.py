#!/usr/bin/python3

# HockeyBox
# by Don Seiler, don@seiler.us
# Based on HockeyBox3.py by Greg Manley
#
# Use 4-space tabs for indentation
# vim :set ts=4 sw=4 sts=4 et:

HOCKEYBOX_VERSION = "202509.1"

from hockeybox_pins import *
from gpiozero import ButtonBoard, LEDBoard, pi_info
from time import sleep
import os, random, vlc
from signal import pause, signal, SIGTERM, SIGHUP, SIGINT
from collections import deque
from pkg_resources import require
from threading import Thread, Event
from rpi_lcd import LCD

pi = pi_info()

print("--------------------------------------------")
print("HockeyBox %s" % HOCKEYBOX_VERSION)
print("by Don Seiler, don@seiler.us")
print("Based on HockeyBox3.py (2016) by Greg Manley")
print("--------------------------------------------")
print("Raspberry Pi Model " + pi.model)
print("gpiozero " + require('gpiozero')[0].version)
print("--------------------------------------------")

#
# LCD Setup
#
lcd_width = 16
lcd_rows = 2
lcd_backlight_enabled = True
lcd = LCD(0x27, 1, lcd_width, lcd_rows, lcd_backlight_enabled)
lcd_event = ""
lcd_song = ""
lcd.text("HockeyBox", 1, 'center')
lcd.text(HOCKEYBOX_VERSION, 2, 'center')
lcd_clear_event = Event() #threading.Event()

# Set thresholds for songs played before a song can be re-played
BTW_REPEAT_THRESHOLD = 50
INTERMISSION_REPEAT_THRESHOLD = 5
GOAL_REPEAT_THRESHOLD = 4
PENALTY_REPEAT_THRESHOLD = 4
POWERPLAY_REPEAT_THRESHOLD = 4

# mp3 locations
BASE_MP3_DIR = "/media/hockeybox"
GOAL_MP3_DIR = BASE_MP3_DIR + "/goal"
BTW_MP3_DIR = BASE_MP3_DIR + "/btw"
INTERMISSION_MP3_DIR = BASE_MP3_DIR + "/intermission"
PENALTY_MP3_DIR = BASE_MP3_DIR + "/penalty"
POWERPLAY_MP3_DIR = BASE_MP3_DIR + "/powerplay"
USANTHEM_MP3_DIR = BASE_MP3_DIR + "/usanthem"

# Queues to track played songs
btw_played_songs = deque([])
intermission_num_played = 0
intermission_played_songs = deque([])
goal_played_songs = deque([])
penalty_played_songs = deque([])
powerplay_played_songs = deque([])

# Setup buttons
buttons = ButtonBoard(
    freebird = BUTTON_FREEBIRD_PIN,
    btw = BUTTON_BTW_PIN,
    intermission = BUTTON_INTERMISSION_PIN,
    goal = BUTTON_GOAL_PIN,
    penalty = BUTTON_PENALTY_PIN,
    powerplay = BUTTON_POWERPLAY_PIN,
    usanthem = BUTTON_USANTHEM_PIN,
    stop = BUTTON_STOP_PIN,
    bounce_time = 0.05
)

# Setup LEDS
leds = LEDBoard(
    btw = LED_BTW_PIN,
    intermission = LED_INTERMISSION_PIN,
    goal = LED_GOAL_PIN,
    penalty = LED_PENALTY_PIN,
    powerplay = LED_POWERPLAY_PIN,
    usanthem = LED_USANTHEM_PIN,
    stop = LED_STOP_PIN,
    _order=('btw','intermission','goal','penalty','powerplay','usanthem','stop')
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

def safe_exit(signum, frame):
    stop_playback()
    lcd.backlight(False)
    lcd.clear()
    exit(1)
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
signal(SIGINT, safe_exit)

#
# lcd_display
# Displays event and song title on 1602 (16 x 2) LCD display
#
def lcd_display():
    global lcd_event, lcd_song, lcd_clear_event

    this_song = lcd_song
    #print("Entering lcd_display() thread. Playing " + this_song)

    lcd.backlight(True)
    lcd.clear()
    lcd.text(lcd_event, 1, 'center')
    while not lcd_clear_event.is_set():
        print(lcd_event + " song playing: " + lcd_song)
        if len(lcd_song) < lcd_width:
            lcd.text(lcd_song, 2)
        else:
            lcd.text(lcd_song[:lcd_width], 2)
            if not lcd_clear_event.is_set():
                sleep(0.5)

            for i in range(len(lcd_song) - lcd_width + 1):
                if lcd_clear_event.is_set():
                    break
                else:
                    sleep(0.25)
                lcd_song_display = lcd_song[i:i+lcd_width]
                lcd.text(lcd_song_display, 2)

        if not lcd_clear_event.is_set():
            sleep(0.5)

    lcd.clear()
    #print("Stopped playing " + this_song + ". Exiting lcd_display() thread")


#
# stop_music_player
#  Checks both players and stops both if necessary
#
def stop_music_player():
    global lcd_clear_event
    lcd_clear_event.set()

    if player.is_playing():
        print("Stopping player")
        player.stop()
    if list_player.is_playing():
        print("Stopping list player")
        list_player.stop()
    print("Music Players Stopped")

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
    # Set lcd_song for display
    global lcd_song
    lcd_song = os.path.basename(p_song)

    # Stop playing if anything is currently playing
    stop_music_player()

    print("Playing %s" % p_song)
    player.set_media(instance.media_new(p_song))
    player.play()

#
# GOAL
#
def play_goal():
    global lcd_event
    lcd_event = "GOAL"
    print(lcd_event)

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
# US ANTHEM
#
def play_usanthem():
    global lcd_event
    lcd_event = "US Anthem"
    print(lcd_event)

    change_lights_after_input(leds.usanthem)
    play_song(pick_random_song(USANTHEM_MP3_DIR))

#
# PENALTY
#
def play_penalty():
    global lcd_event
    lcd_event = "PENALTY"
    print(lcd_event)

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
    global lcd_event
    lcd_event = "POWERPLAY"
    print(lcd_event)

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
    global lcd_event
    lcd_event = "INTERMISSION"
    print(lcd_event)

    change_lights_after_input(leds.intermission)

    # Stop playing if anything is currently playing
    stop_music_player()

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
    global lcd_event
    lcd_event = "BTW"
    print(lcd_event)

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
# FREEBIRD
#
def freebird_time():
    change_lights_after_input(leds.btw)
    freebird_song = "/media/hockeybox/freebird/Free Bird - Rocker Cut.mp3"
    play_song(freebird_song)

#
# STOP
#
def stop_playback():
    # Stop playing if anything is currently playing
    stop_music_player()

    global lcd_event, lcd_song
    lcd_event = "STOP"
    lcd_song = "Music Stopped"
    print(lcd_event)

    cycle_lights_and_on()

    lcd.text(lcd_event, 1, 'center')
    lcd.text(lcd_song, 2,)



# Define event detections and their callbacks
buttons.goal.when_pressed = play_goal
buttons.usanthem.when_pressed = play_usanthem
buttons.penalty.when_pressed = play_penalty
buttons.powerplay.when_pressed = play_powerplay
buttons.intermission.when_pressed = play_intermission
buttons.btw.when_pressed = play_btw
buttons.freebird.when_pressed = freebird_time
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

    global lcd_clear_event, lcd_song
    lcd_song = list_player.get_media_player().get_media().get_meta(0)

    lcd_clear_event.clear()
    lcd_thread = Thread(target=lcd_display, daemon=True)
    lcd_thread.start()

# Update lcd display with what's currently playing
def lcd_update(event):
    global lcd_clear_event, lcd_song

    print("Update LCD")
    lcd_song = player.get_media().get_meta(0)

    lcd_clear_event.clear()
    lcd_thread = Thread(target=lcd_display, daemon=True)
    lcd_thread.start()

# Turn LCD off if nothing has been playing for a while
def lcd_display_off():
    # if the backlight is on but clear event is set,
    # wait 5 seconds, if clear event is still set,
    # turn backlight off
    #
    # XXX:  should probably check if it remained set the whole time
    #       vs could have been started and stopped, which should
    #       reset our timer
    while True:
        if lcd.backlight_status:
            print("LCD backlight is ON")
            if lcd_clear_event.is_set():
                print("LCD clear event is SET")
                sleep(5)
                if lcd_clear_event.is_set():
                    print("LCD clear event is STILL SET, turning backlight OFF")
                    lcd.backlight(False)
        sleep(5)
lcd_off_thread = Thread(target=lcd_display_off, daemon=True)
lcd_off_thread.start()

player_events.event_attach(vlc.EventType.MediaPlayerMediaChanged, lcd_update)
player_events.event_attach(vlc.EventType.MediaPlayerEndReached, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerPlayed, song_finished)
list_events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, intermission_item_played)

# Flicker the lights
print("Light 'em up.")
cycle_lights_and_on()

print("***********************************")
print("HockeyBox ready, waiting for input.")
print("***********************************")

lcd.text("HockeyBox", 1, 'center')
lcd.text("Ready", 2, 'center')
lcd_clear_event.set()

# Pause so event handlers can do the rest
pause()