# Core Game Python by Tanix
#
# 24 Jun 2023

"""renpy
init python:
"""

import json
import logging
import os
import pygame
import os.path
import base64
import os
from datetime import datetime, timedelta
from random import randint, random

SCORE_GOOD = 60
SCORE_PERFECT = 100


class base_class(renpy.python.RevertableObject):

    def __getstate__(self):
        return vars(self).copy()

    def __setstate__(self, new_dict):
        self.__dict__.update(new_dict)

class core(base_class):
    """Game Core Class
    """

    def __init__(self):
        """Game Code Initilalization
        """
        self.tanix_log = self.start_log()
        self.tanix_log.info(f"Starting Game")
        self.images = {}
        self.load_images()
        self.init_values()

    def init_values(self):
        self.up = self.get_image("up.png")
        self.down = self.get_image("down.png")
        self.left = self.get_image("left.png")
        self.right = self.get_image("right.png")
        self.channel = "CHANNEL_RHYTHM_GAME"

        self.content = self.load_content("refdata.json")

        self.score_good = 60
        self.score_perfect = 100
        self.beatmap_stride = 2

    def start_log(self):
        l = logging.getLogger("tanix_log")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fileHandler = logging.FileHandler(f"{config.gamedir}/tanix.log", mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(logging.DEBUG)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

        return logging.getLogger("tanix_log")

    def load_images(self):
        for path in renpy.list_files():
            if path.startswith("images/"):
                path_list = path.split("/")
                self.images[path_list[-1]] = path

    def get_image(self, img):
        if img in self.images:
            output = self.images[img]
        else:
            output = None
        return output

    def load_content(self, datafile):
        with open("{}/{}".format(config.gamedir, datafile), 'rb') as f:
            return json.load(f)

    def load_song(self, song):
        self.rhythm_displayable = RhythmGameDisplayable()
        self.rhythm_displayable.onset_times = self.content["songs"][song]["beatmap"][::self.beatmap_stride]
        self.rhythm_displayable.track_indices = self.content["songs"][song]["tracks"]
        self.rhythm_displayable.audio_path = self.content["songs"][song]["file"]
        self.rhythm_displayable.note_drawables = {0: Image(self.get_image("left.png")),
            1: Image(self.get_image("up.png")),
            2: Image(self.get_image("down.png")),
            3: Image(self.get_image("right.png")),}
        self.rhythm_displayable.set_data()
        self.rhythm_displayable.play_music()
        return self.rhythm_displayable

    def final_score(self, score):
        return round(score / float(self.max_score) * 100)

class RhythmGameDisplayable(renpy.Displayable):

    def __init__(self):
        super(RhythmGameDisplayable, self).__init__()

        self.audio_path = ""
        self.onset_times = []
        self.track_indices = []
        self.note_drawables = {}
        self.channel = "CHANNEL_RHYTHM_GAME"

    def set_data(self):
        self.has_game_started = False
        self.has_music_started = False
        self.has_ended = False
        self.time_offset = None

        self.silence_offset_start = 4.5
        self.silence_start = '<silence %s>' % str(self.silence_offset_start)
        self.countdown = 3.0

        self.x_offset = 400
        self.track_bar_height = int(config.screen_height * 0.85)
        self.track_bar_width = 12
        self.horizontal_bar_height = 8

        self.note_width = 50
        self.zoom_scale = 1.2
        self.note_xoffset = (self.track_bar_width - self.note_width) / 2
        self.note_xoffset_large = (self.track_bar_width - self.note_width * self.zoom_scale) / 2
        self.hit_text_yoffset = 30
        self.note_offset = 3.0
        self.note_speed = config.screen_height / self.note_offset
        self.num_track_bars = 4
        self.track_bar_spacing = (config.screen_width - self.x_offset * 2) / (self.num_track_bars - 1)
        self.track_xoffsets = {
            track_idx: self.x_offset + track_idx * self.track_bar_spacing
            for track_idx in range(self.num_track_bars)
        }

        self.active_notes_per_track = {
            track_idx: [] for track_idx in range(self.num_track_bars)
        }
        self.onset_hits = {
            onset: None for onset in self.onset_times
        }
        self.score = 0
        self.prehit_miss_threshold = 0.4
        self.hit_threshold = 0.3
        self.perfect_threshold = 0.1

        self.keycode_to_track_idx = {
            pygame.K_LEFT: 0,
            pygame.K_UP: 1,
            pygame.K_DOWN: 2,
            pygame.K_RIGHT: 3
        }

        # Displayable elements
        self.miss_text_drawable = Text('Miss!', color='#fff', size=20)  # small text
        self.good_text_drawable = Text('Good!', color='#fff', size=30)  # big text
        self.perfect_text_drawable = Text('Perfect!', color='#fff', size=40)  # bigger text
        self.track_bar_drawable = Solid('#66000000', xsize=self.track_bar_width, ysize=self.track_bar_height)
        self.horizontal_bar_drawable = Solid('#5d01016b', xsize=config.screen_width,
                                             ysize=self.horizontal_bar_height)

        self.note_drawables_large = {
            0: Transform(self.note_drawables[0], zoom=self.zoom_scale),
            1: Transform(self.note_drawables[1], zoom=self.zoom_scale),
            2: Transform(self.note_drawables[2], zoom=self.zoom_scale),
            3: Transform(self.note_drawables[3], zoom=self.zoom_scale),
        }

        self.drawables = [
            self.miss_text_drawable,
            self.good_text_drawable,
            self.perfect_text_drawable,
            self.track_bar_drawable,
            self.horizontal_bar_drawable,
        ]
        self.drawables.extend(list(self.note_drawables.values()))
        self.drawables.extend(list(self.note_drawables_large.values()))

    def render(self, width, height, st, at):
        """
        st: A float, the shown timebase, in seconds.
        The shown timebase begins when this displayable is first shown on the screen.
        """
        if self.has_game_started and self.time_offset is None:
            self.time_offset = self.silence_offset_start + st

        render = renpy.Render(width, height)

        if not self.has_music_started:
            countdown_text = None
            time_before_music = self.countdown - st
            if time_before_music > 2.0:
                countdown_text = '3'
            elif time_before_music > 1.0:
                countdown_text = '2'
            elif time_before_music > 0.0:
                countdown_text = '1'
            else:
                self.has_music_started = True
                renpy.restart_interaction()

            if countdown_text is not None:
                render.place(Text(countdown_text, color='#fff', size=48),
                             x=config.screen_width / 2, y=config.screen_height / 2)

        for track_idx in range(self.num_track_bars):
            x_offset = self.track_xoffsets[track_idx]
            render.place(self.track_bar_drawable, x=x_offset, y=0)
        render.place(self.horizontal_bar_drawable, x=0, y=self.track_bar_height)
        if self.has_game_started:
            if renpy.music.get_playing(channel=self.channel) is None:
                self.has_ended = True
                renpy.timeout(0)  # raise an event
                return render

            curr_time = st - self.time_offset
            self.active_notes_per_track = self.get_active_notes_per_track(curr_time)
            for track_idx in self.active_notes_per_track:
                x_offset = self.track_xoffsets[track_idx]
                for onset, note_timestamp in self.active_notes_per_track[track_idx]:
                    if self.onset_hits[onset] is None:
                        if abs(curr_time - onset) <= self.hit_threshold:
                            note_drawable = self.note_drawables_large[track_idx]
                            note_xoffset = x_offset + self.note_xoffset_large
                        else:
                            note_drawable = self.note_drawables[track_idx]
                            note_xoffset = x_offset + self.note_xoffset
                        note_distance_from_top = note_timestamp * self.note_speed
                        y_offset = self.track_bar_height - note_distance_from_top
                        render.place(note_drawable, x=note_xoffset, y=y_offset)
                    elif self.onset_hits[onset] == 'miss':
                        render.place(self.miss_text_drawable, x=x_offset,
                                     y=self.track_bar_height + self.hit_text_yoffset)
                    elif self.onset_hits[onset] == 'good':
                        render.place(self.good_text_drawable, x=x_offset,
                                     y=self.track_bar_height + self.hit_text_yoffset)
                    elif self.onset_hits[onset] == 'perfect':
                        render.place(self.perfect_text_drawable, x=x_offset,
                                     y=self.track_bar_height + self.hit_text_yoffset)
        renpy.redraw(self, 0)
        return render

    def event(self, ev, x, y, st):
        if self.has_ended:
            renpy.restart_interaction()
            return

        if not self.has_game_started or self.time_offset is None:
            return

        if ev.type == pygame.KEYDOWN:
            if not ev.key in self.keycode_to_track_idx:
                return
            track_idx = self.keycode_to_track_idx[ev.key]
            active_notes_on_track = self.active_notes_per_track[track_idx]
            curr_time = st - self.time_offset
            for onset, _ in active_notes_on_track:
                if self.onset_hits[onset] is not None:
                    continue
                time_delta = curr_time - onset
                if -self.perfect_threshold <= time_delta <= self.perfect_threshold:
                    self.onset_hits[onset] = 'perfect'
                    self.score += SCORE_PERFECT
                    renpy.redraw(self, 0)
                    renpy.restart_interaction()
                elif (-self.hit_threshold <= time_delta < self.perfect_threshold) or \
                        (self.perfect_threshold < time_delta <= self.hit_threshold):
                    self.onset_hits[onset] = 'good'
                    self.score += SCORE_GOOD
                    renpy.redraw(self, 0)
                    renpy.restart_interaction()
                elif (-self.prehit_miss_threshold <= time_delta < -self.hit_threshold):
                    self.onset_hits[onset] = 'miss'
                    renpy.redraw(self, 0)
                    renpy.restart_interaction()

    def visit(self):
        return self.drawables

    def play_music(self):
        renpy.music.queue([self.silence_start, self.audio_path], channel=self.channel, loop=False)
        self.has_game_started = True

    def get_active_notes_per_track(self, current_time):
        active_notes = {
            track_idx: [] for track_idx in range(self.num_track_bars)
        }

        for onset, track_idx in zip(self.onset_times, self.track_indices):
            time_before_appearance = onset - current_time
            if time_before_appearance < 0:
                continue
            elif time_before_appearance <= self.note_offset:
                active_notes[track_idx].append((onset, time_before_appearance))
            elif time_before_appearance > self.note_offset:
                break

        return active_notes

game_core = core()
config.developer = True
renpy.music.register_channel(game_core.channel)
