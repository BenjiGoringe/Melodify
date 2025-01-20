import pygame
import logging

from .settings import (
    AMOUNT_OF_NOTES,
    TARGET_HEIGHT,
    WIDTH,
    WIDTH_SCALE,
    NOTE_SPEED,
    NOTE_DISPLAY_HEIGHT,
    GHOST_FADE_TIME,
    CIRCLE_FADE_TIME,
)
from .note_data import NoteData
from .note_data import Tone

logger = logging.getLogger(__name__)

WHITE_KEYS = Tone.white_keys()
BLACK_KEYS = Tone.black_keys()


def drawPiano(
    screen,
    width,
    height,
    pressed_keys,
    font,
    piano_height,
    key_feedback=None,
):
    line_width = 3
    key_width = width // AMOUNT_OF_NOTES
    black_key_width = key_width // 2
    white_key_height = piano_height
    black_key_height = int(piano_height * 0.6)
    white_base_y = height - piano_height
    black_base_y = height - piano_height

    white_key_labels = {
        k.name: font.render(k.name, True, (0, 0, 0)) for k in WHITE_KEYS
    }
    small_font = pygame.font.Font("freesansbold.ttf", 16)
    black_key_labels = {
        k.name.replace("S", "#"): small_font.render(
            k.name.replace("S", "#"), True, (255, 255, 255)
        )
        for k in BLACK_KEYS
    }

    # WHITE KEYS
    for index, x in enumerate(range(0, width, key_width)):
        tone = WHITE_KEYS[index % 7]
        feedback, _ = key_feedback[tone] if key_feedback else (None, 0)

        # Color logic
        if feedback == "hit":
            key_color = (0, 255, 0)
        elif feedback == "miss":
            key_color = (255, 0, 0)
        elif pressed_keys[tone]:
            key_color = (0, 120, 215)
        else:
            key_color = (255, 255, 255)

        pygame.draw.rect(
            screen, key_color, (x, white_base_y, key_width, white_key_height)
        )
        if x != 0:
            pygame.draw.line(
                screen, (0, 0, 0), (x, white_base_y), (x, height), line_width
            )

        # White key label
        label_surf = white_key_labels[tone.name]
        label_rect = label_surf.get_rect(
            center=(x + key_width // 2, white_base_y + white_key_height * 0.8)
        )
        screen.blit(label_surf, label_rect)

    # BLACK KEYS
    for index, x in enumerate(range(0, width, key_width)):
        tone = WHITE_KEYS[index % 7]
        # If E or B, skip drawing a black key
        if tone in (Tone.E, Tone.B):
            continue

        black_x = x + int(key_width * 0.75)

        black_tone_value = (tone.value + 1) % 12
        black_tone = Tone(black_tone_value)

        feedback, _ = key_feedback[black_tone] if key_feedback else (None, 0)
        if feedback == "hit":
            black_color = (0, 255, 0)
        elif feedback == "miss":
            black_color = (255, 0, 0)
        elif pressed_keys.get(black_tone, False):
            black_color = (0, 120, 215)
        else:
            black_color = (0, 0, 0)

        # Draw the black key with an outline
        outline_rect = pygame.Rect(
            black_x, black_base_y, black_key_width, black_key_height
        )
        pygame.draw.rect(screen, (0, 0, 0), outline_rect)  # Black outline
        inner_rect = outline_rect.inflate(
            -line_width * 2, -line_width * 2
        )  # Actual key rectangle
        pygame.draw.rect(screen, black_color, inner_rect)

        # Black key label
        label_surf = black_key_labels[black_tone.name.replace("S", "#")]
        label_rect = label_surf.get_rect(
            center=(
                black_x + black_key_width // 2,
                black_base_y + black_key_height - 15,
            )
        )
        screen.blit(label_surf, label_rect)

    pygame.draw.line(
        screen, (0, 0, 0), (width, white_base_y), (width, height), line_width
    )
    for i, color in enumerate([(255, 0, 0), (0, 255, 0)]):
        pygame.draw.rect(
            screen, color, (0, white_base_y - (i + 1) * 50, width, TARGET_HEIGHT)
        )
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (0, white_base_y - (i + 1) * 50),
            (width, white_base_y - (i + 1) * 50),
            line_width,
        )
    pygame.draw.line(
        screen, (0, 0, 0), (0, white_base_y), (width, white_base_y), line_width
    )


def drawHealth(screen, health_bar_width, health, max_health) -> None:
    """
    Draw the health bar at the top-left.
    """
    healthX = 12
    healthY = 10
    bar_height = 20
    borderWidth = 3
    pygame.draw.rect(
        screen, (0, 0, 0), (healthX, healthY, health_bar_width, bar_height)
    )
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (
            healthX + borderWidth,
            healthY + borderWidth,
            health_bar_width - borderWidth * 2,
            bar_height - borderWidth * 2,
        ),
    )

    # Red fill
    if max_health > 0:
        fill_width = int((health / max_health) * (health_bar_width - borderWidth * 2))
        pygame.draw.rect(
            screen,
            (255, 0, 0),
            (
                healthX + borderWidth,
                healthY + borderWidth,
                fill_width,
                bar_height - borderWidth * 2,
            ),
        )


def labelsForNotes(screen, width: int, height: int, font) -> None:
    key_width = width // AMOUNT_OF_NOTES
    offset = 520
    note_names = ["C", "D", "E", "F", "G", "A", "B", "C", "D", "E", "F", "G"]
    for index, note in enumerate(note_names):
        note_text = font.render(note, True, (0, 0, 0))
        text_rect = note_text.get_rect(
            center=(index * key_width + key_width // 2, height - offset)
        )
        screen.blit(note_text, text_rect)


def drawScale(screen, width: int, height: int) -> None:
    colour = (255, 255, 255)
    key_width = width // AMOUNT_OF_NOTES
    for x in range(0, width, key_width):
        pygame.draw.rect(screen, colour, (x, 0, key_width, height))
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height), 1)
        colour = (212, 212, 212) if colour == (255, 255, 255) else (255, 255, 255)


def drawNote(screen, note: NoteData, beat_time: float) -> None:
    note_x_list = note.tone.toX(widthScale=WIDTH_SCALE)
    note_y = beatsToY(note.time, beat_time)
    pygame.draw.circle(screen, note.colour, (note_x_list[0], note_y), 10)


def draw_ghosts(screen, ghosts):
    """
    Draws each ghost note as a ring at the point of it being hit.
    ghosts is a list of dicts: {tone, color, frames_left, y_position}.
    """
    for ghost in ghosts:
        tone = ghost["tone"]
        color = ghost["color"]
        frames_left = ghost["frames_left"]
        ghost_y = ghost["y_position"]

        # Calculate opacity, radius and thickness, which face over time
        alpha = int(128 * (frames_left / GHOST_FADE_TIME))  # 50% opacity
        radius = int(10 + (30 - 10) * (1 - frames_left / GHOST_FADE_TIME))
        thickness = max(1, int(5 - 4 * (1 - frames_left / GHOST_FADE_TIME)))

        # Get x-coordinate of the tone
        note_x_list = tone.toX(widthScale=WIDTH_SCALE)

        # Draw ghost
        for x in note_x_list:
            # Create trans surface
            surface_size = (radius + 3) * 2  # Radius + circle thickness
            ghost_surface = pygame.Surface(
                (surface_size, surface_size), pygame.SRCALPHA
            )
            pygame.draw.circle(
                ghost_surface,
                (*color, alpha),
                (surface_size // 2, surface_size // 2),
                radius,
                thickness,
            )

            screen.blit(
                ghost_surface, (x - surface_size // 2, ghost_y - surface_size // 2)
            )


def drawTime(screen, time: float, font) -> None:
    note_text = font.render(f"{int(time)}", True, (0, 0, 0))
    text_rect = note_text.get_rect(center=(100, 100))
    screen.blit(note_text, text_rect)


def drawBeats(screen, visible_beat_count: int, beat_time: float) -> None:
    current_beat = beat_time // 1

    for beat in range(0, visible_beat_count):
        offset = beatsToY(current_beat + beat, beat_time)
        pygame.draw.line(screen, (0, 0, 0, 128), (0, offset), (WIDTH, offset), 2)


def beatsToY(target_beat: float, beat_time: float) -> float:
    return NOTE_SPEED * (beat_time - target_beat) + NOTE_DISPLAY_HEIGHT


def drawProgressBar(
    screen: pygame.Surface,
    segments: list[dict],
    current_time: float,
    total_time: float,
    old_circle_color: tuple[int, int, int],
    new_circle_color: tuple[int, int, int],
    circle_fade_start: float,
) -> None:
    bar_height = 15
    bar_y = 35
    barIndent = 30
    bar_width = screen.get_width() - barIndent
    bar_x = barIndent / 2
    borderWidth = 3

    # Outline and background
    pygame.draw.rect(
        screen,
        (0, 0, 0),
        (
            bar_x - borderWidth,
            bar_y - borderWidth,
            bar_width + borderWidth * 2,
            bar_height + borderWidth * 2,
        ),
        borderWidth * 2,
    )
    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height))

    # Draw each segment
    for i, seg in enumerate(segments):
        seg_start = seg["start"]
        seg_end = seg["end"]
        seg_color = seg["color"]

        if seg_end is None:
            seg_end = current_time

        if seg_end <= seg_start:
            continue
        if seg_start > total_time:
            continue

        draw_start = max(0, seg_start)
        draw_end = min(seg_end, total_time)
        if draw_end <= draw_start:
            continue

        proportion_start = draw_start / total_time
        proportion_end = draw_end / total_time
        px_start = bar_x + int(proportion_start * bar_width)
        px_end = bar_x + int(proportion_end * bar_width)

        if i < len(segments) - 1:
            boundary_beat = seg_end
            boundary_prop = boundary_beat / total_time
            boundary_px = bar_x + int(boundary_prop * bar_width)

            final_end = max(px_start, boundary_px - 10)
            if final_end > px_start:
                pygame.draw.rect(
                    screen,
                    seg_color,
                    (px_start, bar_y, final_end - px_start, bar_height),
                )

            if i + 1 < len(segments):
                next_color = segments[i + 1]["color"]
                blend_start = max(px_start, boundary_px - 10)
                blend_end = min(px_end, boundary_px + 10)
                region_width = blend_end - blend_start
                if region_width > 0:
                    for step in range(int(region_width)):
                        t = step / region_width
                        r = int(seg_color[0] * (1 - t) + next_color[0] * t)
                        g = int(seg_color[1] * (1 - t) + next_color[1] * t)
                        b = int(seg_color[2] * (1 - t) + next_color[2] * t)
                        pygame.draw.line(
                            screen,
                            (r, g, b),
                            (blend_start + step, bar_y),
                            (blend_start + step, bar_y + bar_height),
                        )

            remaining_start = boundary_px + 10
            if remaining_start < px_end:
                pygame.draw.rect(
                    screen,
                    seg_color,
                    (remaining_start, bar_y, px_end - remaining_start, bar_height),
                )
        else:
            pygame.draw.rect(
                screen, seg_color, (px_start, bar_y, px_end - px_start, bar_height)
            )

    fade_delta = current_time - circle_fade_start
    if fade_delta < 0:
        fade_delta = 0
    if fade_delta >= CIRCLE_FADE_TIME:
        circle_color = new_circle_color
    else:
        t = fade_delta / CIRCLE_FADE_TIME
        circle_color = (
            int(old_circle_color[0] * (1 - t) + new_circle_color[0] * t),
            int(old_circle_color[1] * (1 - t) + new_circle_color[1] * t),
            int(old_circle_color[2] * (1 - t) + new_circle_color[2] * t),
        )
        logger.debug(f"Fade delta: {fade_delta}, t: {t}, Circle color: {circle_color}")

    current_prop = min(max(0, current_time / total_time), 1.0)
    circle_x = bar_x + int(current_prop * bar_width)
    circle_y = bar_y + bar_height // 2
    pygame.draw.circle(screen, (255, 255, 255), (circle_x, circle_y), 7)
    pygame.draw.circle(screen, circle_color, (circle_x, circle_y), 4)


def drawScore(screen, score, width, font):
    text_str = f"Score: {score}"
    text_surf = font.render(text_str, True, (0, 0, 0))
    text_rect = text_surf.get_rect(topright=(width - 15, 10))
    screen.blit(text_surf, text_rect)


def drawTopBackground(screen):
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH_SCALE * AMOUNT_OF_NOTES, 60))
    pygame.draw.line(screen, (0, 0, 0), (0, 60), (WIDTH_SCALE * AMOUNT_OF_NOTES, 60), 3)
