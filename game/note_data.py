from __future__ import annotations
from warnings import deprecated
from enum import Enum
import json
from pathlib import Path
from typing import Any, Optional
from pygame import constants
from mido import MidiFile, Message, MidiTrack

try:
    from .settings import NOTE_BEAT_FORGIVENESS
except:
    from settings import NOTE_BEAT_FORGIVENESS
DEFAULT_PATH = Path("branches/")

MIDIBEATLENGTH = 480


# TODO: Perhaps Code a single Octave? (then wraparound mapping for MIDI)
class Tone(Enum):
    C = 0
    CS = 1
    D = 2
    DS = 3
    E = 4
    F = 5
    FS = 6
    G = 7
    GS = 8
    A = 9
    AS = 10
    B = 11

    # Tones fetched from Octave 3 on https://muted.io/note-frequencies/
    @property
    def freq(self) -> float:
        TONEFREQUENCYMAP: dict[Tone, float] = {
            Tone.C: 130.81,
            Tone.CS: 138.59,
            Tone.D: 146.83,
            Tone.DS: 155.56,
            Tone.E: 164.81,
            Tone.F: 174.61,
            Tone.FS: 185,
            Tone.G: 196,
            Tone.GS: 207.65,
            Tone.A: 220,
            Tone.AS: 233.08,
            Tone.B: 246.94,
        }
        return TONEFREQUENCYMAP[self]

    def toX(self, widthScale: int) -> list[int]:
        TONEXMAP: dict[Tone, list[int]] = {
            Tone.C: [
                (widthScale * 0) + int(widthScale / 2),
                (widthScale * 7) + int(widthScale / 2),
            ],
            Tone.CS: [(widthScale * 0) + widthScale],
            Tone.D: [(widthScale * 1) + int(widthScale / 2)],
            Tone.DS: [(widthScale * 1) + widthScale],
            Tone.E: [(widthScale * 2) + int(widthScale / 2)],
            Tone.F: [(widthScale * 3) + int(widthScale / 2)],
            Tone.FS: [(widthScale * 3) + widthScale],
            Tone.G: [(widthScale * 4) + int(widthScale / 2)],
            Tone.GS: [(widthScale * 4) + widthScale],
            Tone.A: [(widthScale * 5) + int(widthScale / 2)],
            Tone.AS: [(widthScale * 5) + widthScale],
            Tone.B: [(widthScale * 6) + int(widthScale / 2)],
        }
        return TONEXMAP[self]

    @deprecated("Keyboard input no longer supported")
    def keyboard_key(self) -> Optional[int]:
        TONEKEYBOARDMAP: dict[Tone, int] = {
            Tone.C: constants.K_1,
            Tone.D: constants.K_2,
            Tone.E: constants.K_3,
            Tone.F: constants.K_4,
            Tone.G: constants.K_5,
            Tone.A: constants.K_6,
            Tone.B: constants.K_7,
        }
        return TONEKEYBOARDMAP[self]

    def __str__(self) -> str:
        return self.name

    @deprecated("Keyboard input no longer supported")
    # Method can return None if key does not have mapped Keyboard Tone
    @staticmethod
    def fromKey(key: int) -> Optional[Tone]:
        KEYBOARDTONEMAP: dict[int, Tone] = {
            constants.K_1: Tone.C,
            constants.K_2: Tone.D,
            constants.K_3: Tone.E,
            constants.K_4: Tone.F,
            constants.K_5: Tone.G,
            constants.K_6: Tone.A,
            constants.K_7: Tone.B,
            constants.K_8: Tone.C,
            constants.K_9: Tone.D,
            constants.K_0: Tone.E,
        }
        return KEYBOARDTONEMAP.get(key, None)

    @staticmethod
    def fromID(string: str) -> Tone:
        return Tone(Tone._member_names_.index(string))

    @staticmethod
    def fromMidi(midi_key: int) -> Tone:
        return Tone(midi_key % 12)

    @staticmethod
    def keys() -> list[Tone]:
        return [
            Tone.C,
            Tone.CS,
            Tone.D,
            Tone.DS,
            Tone.E,
            Tone.F,
            Tone.FS,
            Tone.G,
            Tone.GS,
            Tone.A,
            Tone.AS,
            Tone.B,
        ]

    @staticmethod
    def white_keys() -> list[Tone]:
        return [Tone.C, Tone.D, Tone.E, Tone.F, Tone.G, Tone.A, Tone.B]

    @staticmethod
    def black_keys() -> list[Tone]:
        return [Tone.CS, Tone.DS, Tone.FS, Tone.GS, Tone.AS]


class NoteData:
    def __init__(
        self,
        time: float,  # In terms of beats (0.5 beats is a 'quaver'), start of branch: 0
        duration: float,  # How long to hold note (not used)
        tone: Tone,  # Tone of Note (for example C, or C#)
        branch: Branch,  # Set by parent branch
    ) -> None:
        self.time = time
        self.duration = duration
        self.tone = tone
        self.branch = branch
        # TODO give branches colours (branch is a string+int)

    def toDict(self) -> dict[str, Any]:
        return {
            "time": self.time,
            "duration": self.duration,
            "tone": self.tone.name,
            "branch": self.branch,
        }

    @staticmethod
    def fromDict(note_dict: dict[str, Any]) -> NoteData:
        return NoteData(
            note_dict["time"],
            note_dict["duration"],
            Tone.fromID(note_dict["tone"]),
            note_dict["branch"],
        )

    def isHittable(self, beat_time: float) -> bool:
        min_time = beat_time - NOTE_BEAT_FORGIVENESS
        max_time = beat_time + NOTE_BEAT_FORGIVENESS
        return min_time < self.time and self.time < max_time

    def isOffScreen(self, beat_time: float) -> bool:
        max_time = beat_time - NOTE_BEAT_FORGIVENESS
        return self.time < max_time

    @property
    def colour(self) -> tuple[int, int, int]:
        return self.branch.colour

    def applyTimeOffset(self, offset: float) -> NoteData:
        return NoteData(self.time + offset, self.duration, self.tone, self.branch)


type Notes = list[NoteData]


class Branch:
    def __init__(self, id: int, name: str, start_time: float):
        # ID: 0-7
        self.id = id
        # Filename (e.g. Chorus1, Verse1 etc.)
        self.name = name
        # Start Time of Branch (to offset note values on init)
        self.start_time = start_time
        # Calculated from Midi Notes
        self._notes = self.loadMidi()
        self.metadata = self.loadDict()
        # Calculated on load from Midi Contents
        # self.duration = self.calculate
        # Next Branch (points to next .json file)
        self.next_branch_name: str | None = (
            self.metadata["next_branch"] if self.metadata != "None" else None
        )
        # Colour of notes: (e.g. 0xFF00FF), type is of tuple so that
        # Left and Right branches can be distinguished
        colours = [
            (0, 0, 0),  # Black
            (0, 0, 255),  # Red
            (0, 255, 0),  # Green
            (255, 0, 0),  # Blue
            (150, 150, 0),  # Yellow
            (0, 150, 150),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 0, 255),  # Orange
        ]
        self.colour = colours[(self.id + sum(ord(char) for char in self.name)) % 7]

    @property
    def identifier(self) -> str:
        return f"{self.name}{self.id}"

    @property
    def next_branch_ids(self) -> tuple[int, int]:
        return (self.id * 2 - 1, self.id * 2)

    def loadDict(self) -> dict[str, Any]:
        with open(DEFAULT_PATH / "json" / f"{self.name}.json") as jsonFile:
            data = json.load(jsonFile)
        return data

    def loadMidi(self) -> Notes:
        on_off: dict[Tone, int | None] = {tone: 0 for tone in Tone}
        notes: Notes = []
        filepath = DEFAULT_PATH / "midi" / f"{self.name}.mid"
        midifile = MidiFile(filepath)
        branch: MidiTrack = midifile.tracks[self.id % len(midifile.tracks)]
        events: list[dict[str, Any]] = [
            event.dict()
            for event in filter(
                lambda m: isinstance(m, Message), [message for message in branch]
            )
        ]
        current_time = 0
        for event in events:
            current_time += int(event["time"])
            current_tone = Tone.fromMidi(int(event["note"]))
            match (event["type"]):
                case "note_on":
                    if not on_off[current_tone]:
                        on_off[current_tone] = current_time
                case "note_off":
                    if start_time := on_off[current_tone]:
                        notes.append(
                            NoteData(
                                time=(start_time / MIDIBEATLENGTH),
                                duration=(current_time - start_time) / MIDIBEATLENGTH,
                                tone=current_tone,
                                branch=self,
                            )
                        )
                        on_off[current_tone] = None
                    else:
                        # Assume a mismatched note off means that the note began at the start of the midi track
                        notes.append(
                            NoteData(
                                time=0,
                                duration=(current_time) / MIDIBEATLENGTH,
                                tone=current_tone,
                                branch=self,
                            )
                        )
        # Hacky code to remove 'whitespace'
        # if len(notes) >= 1:
        #     offset = notes[0].time
        # for i in range(1, len(notes)):
        #     notes[i].time -= offset
        return notes

    @property
    def duration(self) -> float:
        if not self._notes:
            return 0.0
        final_note = sorted(self._notes, key=lambda note: note.time, reverse=True)[0]
        return final_note.time + final_note.duration

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration

    @property
    def notes(self) -> list[NoteData]:
        return list(
            map(lambda note: note.applyTimeOffset(self.start_time), self._notes)
        )


if __name__ == "__main__":

    # print(list(Tone.__iter__()))

    # Example of a Branch being loaded
    new_branch1 = Branch(0, "a", 0)
    new_branch2 = Branch(1, "b", new_branch1.end_time)
    new_branch3 = Branch(2, "b", 10)
    print(f"{new_branch1.name}, {new_branch1.id} : {new_branch1.colour}")
    for note in new_branch1.notes:
        print(f"{note.time:>5} : {note.duration} : {note.tone.name}")
    print(f"{new_branch2.name}, {new_branch2.id} : {new_branch2.colour}")
    for note in new_branch2.notes:
        print(f"{note.time:>5} : {note.duration} : {note.tone.name}")
    print(f"{new_branch3.name}, {new_branch3.id} : {new_branch3.colour}")
    for note in new_branch3._notes:
        print(f"{note.time:>5} : {note.duration} : {note.tone.name}")
    for note in new_branch3.notes:
        print(f"{note.time:>5} : {note.duration} : {note.tone.name}")
    for note in new_branch3._notes:
        print(f"{note.time:>5} : {note.duration} : {note.tone.name}")
