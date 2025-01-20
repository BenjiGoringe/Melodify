from typing import Literal
import pygame
import pygame.midi
from enum import Enum
from pathlib import Path
import logging

from .settings import (
    HEIGHT,
    WIDTH_SCALE,
    AMOUNT_OF_NOTES,
    BPM,
    MAX_HEALTH,
    MUSIC_FILE,
    MIDI,
    KEY_FLASH_TIME,
    GHOST_FADE_TIME,
    SCORE_INCREMENT,
    MIDI_DEVICES,
)
from .subScreens import (
    draw_home_screen,
    handle_home_screen_click,
    draw_game_over_screen,
    handle_game_over_screen_click,
    draw_pause_screen,
    handle_pause_screen_click,
    draw_countdown_screen,
    draw_song_selection_screen,
    handle_song_selection_screen_click,
    draw_leaderboard_screen,
    handle_leaderboard_screen_click,
    draw_tutorial_screen,
    handle_tutorial_screen_click,
    draw_settings_screen,
    handle_settings_screen_click,
)
from .player import Music
from .ui import (
    drawBeats,
    drawScale,
    drawPiano,
    drawHealth,
    labelsForNotes,
    drawNote,
    draw_ghosts,
    beatsToY,
    drawProgressBar,
    drawScore,
    drawTopBackground,
)
from .note_data import NoteData, Branch, Tone

logger = logging.getLogger(__name__)


class GameState(Enum):
    HOME = 0
    SONG_SELECTION = 1
    PLAYING = 2
    PAUSE = 3
    COUNTDOWN = 4
    GAME_OVER = 5
    QUIT = 6
    LEADERBOARD = 7
    TUTORIAL = 8
    SETTINGS = 9


class Game:
    def __init__(self):
        pygame.init()
        pygame.midi.init()
        MIDI_DEVICES.clear()
        for i in range(pygame.midi.get_count()):
            info = pygame.midi.get_device_info(i)
            is_input = bool(info[2])
            if is_input:
                device_name = info[1].decode()
                MIDI_DEVICES.append(device_name)

        self.width = AMOUNT_OF_NOTES * WIDTH_SCALE
        self.height = HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Melodify")
        logo = pygame.image.load("./logo_sm.png")
        pygame.display.set_icon(logo)

        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.HOME

        self.time = 0.0
        pygame.font.init()
        self.font = pygame.font.Font("freesansbold.ttf", 32)

        self.scoreFont = pygame.font.Font("freesansbold.ttf", 20)
        self.white_font = pygame.font.Font("freesansbold.ttf", 20)

        self.health = MAX_HEALTH
        self.colour_flash = None
        self.flash_timer = 0

        self.pressedKeys: dict[Tone, bool] = {tone: False for tone in Tone}

        # Per-key feedback: tone -> ("hit"/"miss", frames_left), or (None, 0) if no feedback
        self.key_feedback: dict[
            Tone, tuple[Literal["hit"] | Literal["miss"] | None, int]
        ] = {tone: (None, 0) for tone in Tone}

        self.music = Music(Path(MUSIC_FILE))

        self.speed = int(60000 / BPM)

        # Branch/notes
        self.currentBranch = Branch(0, "a", start_time=4)
        next_branch_name = (
            self.currentBranch.next_branch_name or self.currentBranch.name
        )
        if next_branch_name:
            self.queuedBranches = (
                Branch(1, next_branch_name, start_time=self.currentBranch.end_time),
                Branch(2, next_branch_name, start_time=self.currentBranch.end_time),
            )
        else:
            self.queuedBranches = None
        self.notes = self.melody()

        if MIDI:
            self.midiInput = self.midiConnect()
        else:
            logger.debug("MIDI disabled")

        # Pause / Countdown
        self.paused_background = None
        self.countdown_value = 3
        self.countdown_start_time = 0

        self.ghosts = []  # Dict: {tone, color, frames_left}

        # Each segment: {start: time_in_beats, end: optional_time_in_beats or None, color, fade_start: None/int}
        # The last segment is active if 'end' is None
        self.progress_segments = [
            {
                "start": 0.0,
                "end": None,
                "color": self.currentBranch.colour,
            }
        ]
        self.old_circle_color = self.currentBranch.colour
        self.circle_fade_start = 0.0

        # Score & Leaderboard
        self.score = 0
        self.game_over_score = 0
        self.leaderboard = []  # Store all final scores TODO: Actually save it

        logger.debug("Game initialized")

    def run(self):
        """
        Main game loop: Poll events, update the current state, draw everything, then flip the display.
        """
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    old_state = self.state
                    self.state = GameState.QUIT
                    if old_state != self.state:
                        logger.info(f"State changed: {old_state} -> {self.state}")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    if self.state == GameState.PLAYING:
                        old_state = self.state
                        self.enter_pause()
                        self.music.pause()
                        self.music.paused = True
                        logger.info(f"State changed: {old_state} -> {self.state}")
                    elif self.state == GameState.PAUSE:
                        old_state = self.state
                        self.enter_countdown()
                        logger.info(f"State changed: {old_state} -> {self.state}")
                    elif self.state == GameState.COUNTDOWN:
                        old_state = self.state
                        self.state = GameState.PAUSE
                        logger.info(f"State changed: {old_state} -> {self.state}")

            if self.state == GameState.HOME:
                draw_home_screen(self.screen, self.font)
                action = handle_home_screen_click(events)
                if action == "start":
                    logger.info(f"State changed: {self.state} -> SONG_SELECTION")
                    self.state = GameState.SONG_SELECTION
                elif action == "tutorial":
                    old_state = self.state
                    self.state = GameState.TUTORIAL
                    logger.info(f"State changed: {old_state} -> {self.state}")
                elif action == "settings":
                    self.state = GameState.SETTINGS
                elif action == "quit":
                    old_state = self.state
                    self.state = GameState.QUIT
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.SONG_SELECTION:
                draw_song_selection_screen(self.screen, self.font)
                song_action = handle_song_selection_screen_click(events)
                if song_action == "back":
                    old_state = self.state
                    self.state = GameState.HOME
                    logger.info(f"State changed: {old_state} -> {self.state}")
                elif song_action and song_action.startswith("song:"):
                    # E.g. "song:Song A"
                    chosen_song = song_action.split("song:")[1]
                    logger.info(f"Song chosen: {chosen_song}")
                    # Temp, just reset game with that as a branch name TODO: Change
                    self.reset_game_for_song(chosen_song.lower()[-1])
                    old_state = self.state
                    self.state = GameState.PLAYING
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.TUTORIAL:
                draw_tutorial_screen(self.screen, self.font)
                lb_action = handle_tutorial_screen_click(events)
                if lb_action == "back":
                    old_state = self.state
                    self.state = GameState.HOME
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.PLAYING:
                self.update_pressed_keys()
                self.update_game()
                self.draw_game()

            elif self.state == GameState.PAUSE:
                draw_pause_screen(self.screen, self.paused_background, self.font)
                pause_action = handle_pause_screen_click(events)
                if pause_action == "resume":
                    old_state = self.state
                    self.enter_countdown()
                    logger.info(f"State changed: {old_state} -> {self.state}")
                elif pause_action == "home":
                    old_state = self.state
                    self.state = GameState.HOME
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.COUNTDOWN:
                self.update_countdown()
                draw_countdown_screen(
                    self.screen, self.paused_background, self.countdown_value
                )

            elif self.state == GameState.GAME_OVER:
                self.music.stop()
                # Pass the final score (game_over_score) to the draw function
                draw_game_over_screen(self.screen, self.font, self.game_over_score)
                action = handle_game_over_screen_click(events)
                if action == "again":
                    self.reset_game()
                    old_state = self.state
                    self.state = GameState.HOME
                    logger.info(f"State changed: {old_state} -> {self.state}")
                elif action == "leaderboard":
                    old_state = self.state
                    self.state = GameState.LEADERBOARD
                    logger.info(f"State changed: {old_state} -> {self.state}")
                elif action == "quit":
                    old_state = self.state
                    self.state = GameState.QUIT
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.LEADERBOARD:
                draw_leaderboard_screen(self.screen, self.font, self.leaderboard)
                lb_action = handle_leaderboard_screen_click(events, self.screen)
                if lb_action == "back":
                    old_state = self.state
                    self.state = GameState.GAME_OVER
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.SETTINGS:
                draw_settings_screen(self.screen, self.font)
                settings_action = handle_settings_screen_click(events)
                if settings_action == "back":
                    old_state = self.state
                    self.state = GameState.HOME
                    logger.info(f"State changed: {old_state} -> {self.state}")

            elif self.state == GameState.QUIT:
                self.running = False

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def reset_game_for_song(self, song_name: str):
        """
        Similar to reset_game, but loads 'song_name' as the branch name.
        """
        self.health = MAX_HEALTH
        self.time = 0
        self.colour_flash = None
        self.flash_timer = 0
        self.music.stop()
        self.music.play()

        self.score = 0
        self.game_over_score = 0

        self.currentBranch = Branch(0, song_name, start_time=4)
        next_branch_name = (
            self.currentBranch.next_branch_name or self.currentBranch.name
        )
        if next_branch_name:
            self.queuedBranches = (
                Branch(1, next_branch_name, start_time=self.currentBranch.end_time),
                Branch(2, next_branch_name, start_time=self.currentBranch.end_time),
            )
        else:
            self.queuedBranches = None

        self.notes = self.melody()

        for tone in self.key_feedback:
            self.key_feedback[tone] = (None, 0)

        self.ghosts.clear()
        self.progress_segments = [
            {
                "start": 0.0,
                "end": None,
                "color": self.currentBranch.colour,
            }
        ]
        self.old_circle_color = self.currentBranch.colour
        self.circle_fade_start = 0.0

    def reset_game(self):
        """
        Reset all necessary variables to start the game again.
        """
        self.health = MAX_HEALTH
        self.time = 0
        self.colour_flash = None
        self.flash_timer = 0
        self.music.stop()

        self.score = 0

        self.currentBranch = Branch(0, "a", start_time=4)
        next_branch_name = (
            self.currentBranch.next_branch_name or self.currentBranch.name
        )
        if next_branch_name:
            self.queuedBranches = (
                Branch(1, next_branch_name, start_time=self.currentBranch.end_time),
                Branch(2, next_branch_name, start_time=self.currentBranch.end_time),
            )
        else:
            self.queuedBranches = None
        self.notes = self.melody()
        for tone in self.key_feedback:
            self.key_feedback[tone] = (None, 0)
        self.ghosts.clear()

        self.progress_segments = [
            {
                "start": 0.0,
                "end": None,
                "color": self.currentBranch.colour,
            }
        ]
        self.old_circle_color = self.currentBranch.colour
        self.circle_fade_start = 0.0

    def update_game(self):
        """
        Update main game logic (timing, note hits, health, branch transitions).
        """
        if self.health <= 0:
            self.music.stop()
            self.game_over_score = self.score
            old_state = self.state
            self.leaderboard.append(self.score)
            self.leaderboard.sort(reverse=True)
            self.state = GameState.GAME_OVER
            logger.info(f"State changed: {old_state} -> {self.state}")
            return

        raw_time_ms = self.clock.get_time()
        self.time += self.time_to_beats(raw_time_ms)
        self.flash_timer -= 1
        if self.flash_timer <= 0:
            self.colour_flash = None

        off_screen_notes = [note for note in self.notes if note.isOffScreen(self.time)]
        for note in off_screen_notes:
            if note in self.notes:
                self.notes.remove(note)
            old_health = self.health
            self.health -= 1
            logger.debug(f"Health changed: {old_health} -> {self.health}")
            self.key_feedback[note.tone] = ("miss", KEY_FLASH_TIME)

        hittable_notes = [note for note in self.notes if note.isHittable(self.time)]
        hit_notes = [note for note in hittable_notes if self.pressedKeys[note.tone]]
        for note in hit_notes:
            # If branch possible
            if note.branch != self.currentBranch:
                # Check for similar hittable notes (inc. note)
                similar_notes = [n for n in hit_notes if n.tone == note.tone]
                # If note is only similar note, switch branch
                if len(similar_notes) == 1:
                    self.nextBranch(note.branch)

            # Mark a "hit"
            self.key_feedback[note.tone] = ("hit", KEY_FLASH_TIME)

            self.score += SCORE_INCREMENT

            ghost_y_position = beatsToY(note.time, self.time)
            self.ghosts.append(
                {
                    "tone": note.tone,
                    "color": (0, 0, 0),
                    "frames_left": GHOST_FADE_TIME,
                    "y_position": ghost_y_position,
                }
            )

        for note in hit_notes:
            if note in self.notes:
                self.notes.remove(note)

        # Decrement each key's flash timer
        for tone, (status, frames_left) in self.key_feedback.items():
            if frames_left > 0:
                self.key_feedback[tone] = (status, frames_left - 1)
            else:
                self.key_feedback[tone] = (None, 0)

        # Decrement ghost frames
        for ghost in self.ghosts:
            ghost["frames_left"] -= 1
        self.ghosts = [g for g in self.ghosts if g["frames_left"] > 0]

        # If no more notes:
        if not self.notes and not self.queuedBranches:
            self.music.stop()
            self.game_over_score = self.score
            old_state = self.state
            self.leaderboard.append(self.score)
            self.leaderboard.sort(reverse=True)
            self.state = GameState.GAME_OVER
            logger.info(f"State changed: {old_state} -> {self.state}")

    def draw_game(self):
        """
        Draw everything for the gameplay state.
        """
        self.screen.fill((255, 255, 255))
        drawScale(self.screen, self.width, self.height)

        drawBeats(self.screen, 5, self.time)

        drawPiano(
            screen=self.screen,
            width=self.width,
            height=self.height,
            pressed_keys=self.pressedKeys,
            font=self.font,
            piano_height=100,
            key_feedback=self.key_feedback,
        )

        for note in self.notes:
            drawNote(self.screen, note, self.time)

        drawTopBackground(self.screen)

        draw_ghosts(self.screen, self.ghosts)

        # Draw health (200px on the right side for the score)
        health_bar_width = self.width - 200
        drawHealth(self.screen, health_bar_width, self.health, MAX_HEALTH)

        # Draw score in the top-right corner
        drawScore(self.screen, self.score, self.width, self.scoreFont)

        drawProgressBar(
            screen=self.screen,
            segments=self.progress_segments,
            current_time=self.time,
            total_time=self.totalSongTime(),
            old_circle_color=self.old_circle_color,
            new_circle_color=self.currentBranch.colour,
            circle_fade_start=self.circle_fade_start,
        )

        labelsForNotes(self.screen, self.width, self.height, self.font)

    def melody(self) -> list[NoteData]:
        """
        Builds or rebuilds the list of notes from current and queued branches then sorts them by note time.
        """
        if self.queuedBranches:
            return sorted(
                self.currentBranch.notes
                + self.queuedBranches[0].notes
                + self.queuedBranches[1].notes,
                key=lambda note: note.time,
            )
        return sorted(self.currentBranch.notes, key=lambda note: note.time)

    def nextBranch(self, next_branch: Branch) -> None:
        """
        Finalise old bit, create new bit and fade circle color from old to new over CIRCLE_FADE_TIME.
        """
        old_branch = self.currentBranch
        old_color = self.currentBranch.colour
        logger.debug(f"Old branch: {old_branch}, Old color: {old_color}")

        # End old segment
        last_seg = self.progress_segments[-1]
        if last_seg["end"] is None:
            last_seg["end"] = self.time

        # Switch
        self.currentBranch = next_branch

        # Start new segment
        self.progress_segments.append(
            {
                "start": self.time,
                "end": None,
                "color": self.currentBranch.colour,
            }
        )

        # Fade circle color
        self.old_circle_color = old_color
        self.circle_fade_start = self.time

        next_branch_name = (
            self.currentBranch.next_branch_name or self.currentBranch.name
        )
        end_time = self.currentBranch.end_time
        id1, id2 = self.currentBranch.next_branch_ids
        if next_branch_name:
            self.queuedBranches = (
                Branch(id1, next_branch_name, start_time=end_time),
                Branch(id2, next_branch_name, start_time=end_time),
            )
        else:
            self.queuedBranches = None
        self.notes = self.melody()

    def update_pressed_keys(self) -> None:
        """
        Poll MIDI data and update which notes are currently pressed.
        """
        if not self.midiInput:
            return
        if not self.midiInput.poll():
            return
        if self.midiInput.poll:
            for event in self.midiInput.read(10):
                data = event[0]
                if isinstance(data, list):
                    status, note, velocity, _ = data
                    tone = Tone.fromMidi(note)
                    logger.debug(
                        f"MIDI event: status={status}, tone={tone}, velocity={velocity}"
                    )
                    if status == 144:
                        self.pressedKeys[tone] = velocity > 0
                    elif status == 128:
                        self.pressedKeys[tone] = False

    def midiConnect(self) -> pygame.midi.Input:
        """
        Tries connecting to the default MIDI input or asks user for device ID if not found.
        """
        logger.info("Checking available MIDI Input Devices...")
        for i in range(pygame.midi.get_count()):
            info = pygame.midi.get_device_info(i)
            if info[2]:
                logger.debug(f"Device #{i}: {info[1].decode()} (Input)")
        input_id = pygame.midi.get_default_input_id()
        if input_id == -1:
            input_id = int(input("Enter the MIDI Input device ID to use: "))
        logger.info(f"Using MIDI device ID: {input_id}")
        return pygame.midi.Input(input_id)

    @staticmethod
    def time_to_beats(raw_time_ms: float) -> float:
        """
        Convert milliseconds into 'beats' based on BPM setting.
        """
        return ((raw_time_ms / 1000.0) / 60.0) * BPM

    def enter_pause(self):
        """
        Switch to PAUSE state, store a blurred background.
        """
        self.state = GameState.PAUSE
        self.draw_game()
        pygame.display.flip()
        self.paused_background = self.create_blurred_surface()

    def enter_countdown(self):
        """
        Switch to COUNTDOWN state and reset countdown.
        """
        self.state = GameState.COUNTDOWN
        self.countdown_value = 3
        self.countdown_start_time = pygame.time.get_ticks()

    def update_countdown(self):
        """
        Decrement the countdown each second. Resume if it reaches 0.
        """
        elapsed = pygame.time.get_ticks() - self.countdown_start_time
        new_val = 3 - (elapsed // 1000)
        if new_val <= 0:
            old_state = self.state
            self.state = GameState.PLAYING
            logger.info(f"State changed: {old_state} -> {self.state}")
            if self.music.paused == True:
                self.music.unpause()
                self.music.paused = False
        else:
            self.countdown_value = new_val

    def create_blurred_surface(self):
        """
        Return a blurred copy of the current screen.
        """
        surface_copy = self.screen.copy()
        w, h = surface_copy.get_size()
        scale = 0.1
        small_w = int(w * scale)
        small_h = int(h * scale)
        small_surf = pygame.transform.smoothscale(surface_copy, (small_w, small_h))
        blurred_surf = pygame.transform.smoothscale(small_surf, (w, h))
        return blurred_surf

    def totalSongTime(self) -> float:
        """
        Calculate estimate for total time in beats for the entire track.
        For demo, guess the end_time of the last branch is the final.
        This doesn't actually work well but it looks good enough.
        """
        candidate_times = [self.currentBranch.end_time]
        if self.queuedBranches:
            for br in self.queuedBranches:
                candidate_times.append(br.end_time)
        return max(candidate_times)
