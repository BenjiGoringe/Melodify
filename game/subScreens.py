import pygame
from .settings import (
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    TITLE_TEXT_COLOR,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_X,
    BUTTON_Y,
    WIDTH_SCALE,
    AMOUNT_OF_NOTES,
    BORDER_WIDTH,
    ENABLE_METRONOME,
    CURRENT_BPM,
    SELECTED_MIDI_DEVICE,
    MIDI_DEVICES,
    MIDI_DROPDOWN_EXPANDED,
    BPM_INPUT_ACTIVE,
    BPM_INPUT_TEXT,
)

button_width = BUTTON_WIDTH
button_height = BUTTON_HEIGHT
button_x = BUTTON_X
button_y = BUTTON_Y

# Temp Song list
SONG_OPTIONS = ["Song A", "Song B", "Song C", "Song D"]


def draw_home_screen(screen: pygame.Surface, font: pygame.font.Font) -> None:
    """
    Draws the home screen with two buttons: 'Start' and 'Quit'.
    Does not handle events or return anything.
    """
    screen.fill((255, 255, 255))

    # Title
    title_text = font.render("Melodify", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(
        center=(button_x + button_width // 2, button_y - 200 + button_height // 2)
    )
    screen.blit(title_text, title_rect)

    mouse_pos = pygame.mouse.get_pos()

    # Start Button
    pygame.draw.rect(
        screen, (0, 0, 0),
        (button_x - BORDER_WIDTH, button_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    )
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and button_y <= mouse_pos[1] <= button_y + button_height):
        pygame.draw.rect(
            screen, BUTTON_HOVER_COLOR,
            (button_x, button_y, button_width, button_height)
        )
    else:
        pygame.draw.rect(
            screen, BUTTON_COLOR,
            (button_x, button_y, button_width, button_height)
        )
    start_text = font.render("Start", True, BUTTON_TEXT_COLOR)
    start_rect = start_text.get_rect(
        center=(button_x + button_width // 2, button_y + button_height // 2)
    )
    screen.blit(start_text, start_rect)

    # Tutorial Button
    tutorial_y = button_y + 75
    pygame.draw.rect(
        screen, (0, 0, 0),
        (button_x - BORDER_WIDTH, tutorial_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    )
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and tutorial_y <= mouse_pos[1] <= tutorial_y + button_height):
        pygame.draw.rect(
            screen, BUTTON_HOVER_COLOR,
            (button_x, tutorial_y, button_width, button_height)
        )
    else:
        pygame.draw.rect(
            screen, BUTTON_COLOR,
            (button_x, tutorial_y, button_width, button_height)
        )
    tutorial_text = font.render("Tutorial", True, BUTTON_TEXT_COLOR)
    tutorial_rect = tutorial_text.get_rect(
        center=(button_x + button_width // 2, tutorial_y + button_height // 2)
    )
    screen.blit(tutorial_text, tutorial_rect)

    # Settings Button
    settings_y = tutorial_y + 75
    pygame.draw.rect(
        screen, (0, 0, 0),
        (button_x - BORDER_WIDTH, settings_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    )
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and settings_y <= mouse_pos[1] <= settings_y + button_height):
        pygame.draw.rect(
            screen, BUTTON_HOVER_COLOR,
            (button_x, settings_y, button_width, button_height)
        )
    else:
        pygame.draw.rect(
            screen, BUTTON_COLOR,
            (button_x, settings_y, button_width, button_height)
        )
    settings_text = font.render("Settings", True, BUTTON_TEXT_COLOR)
    settings_rect = settings_text.get_rect(
        center=(button_x + button_width // 2, settings_y + button_height // 2)
    )
    screen.blit(settings_text, settings_rect)

    # Quit Button
    quit_y = settings_y + 75
    pygame.draw.rect(
        screen, (0, 0, 0),
        (button_x - BORDER_WIDTH, quit_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    )
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and quit_y <= mouse_pos[1] <= quit_y + button_height):
        pygame.draw.rect(
            screen, BUTTON_HOVER_COLOR,
            (button_x, quit_y, button_width, button_height)
        )
    else:
        pygame.draw.rect(
            screen, BUTTON_COLOR,
            (button_x, quit_y, button_width, button_height)
        )
    quit_text = font.render("Quit", True, BUTTON_TEXT_COLOR)
    quit_rect = quit_text.get_rect(
        center=(button_x + button_width // 2, quit_y + button_height // 2)
    )
    screen.blit(quit_text, quit_rect)


def handle_home_screen_click(events) -> str | None:
    """
    Processes events on the home screen.
    Returns:
      "start" if the Start button is clicked,
      "tutorial" if the Tutorial button is clicked,
      "settings" if the Settings button is clicked,
      "quit" if the Quit button is clicked or window closed,
      else None.
    """
    mouse_pos = pygame.mouse.get_pos()
    tutorial_y = button_y + 75
    settings_y = tutorial_y + 75
    quit_y = settings_y + 75

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Start Button
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and button_y <= mouse_pos[1] <= button_y + button_height):
                return "start"

            # Tutorial Button
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and tutorial_y <= mouse_pos[1] <= tutorial_y + button_height):
                return "tutorial"

            # Settings Button
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and settings_y <= mouse_pos[1] <= settings_y + button_height):
                return "settings"

            # Quit Button
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and quit_y <= mouse_pos[1] <= quit_y + button_height):
                return "quit"

        elif event.type == pygame.QUIT:
            return "quit"
    return None


def draw_game_over_screen(screen, font, final_score: int):
    """
    Draws the game-over screen:
      - Displays "Game Over"
      - Displays the player's final_score
      - "Play Again", "Leaderboard", "Quit" buttons
    """
    screen.fill((255, 255, 255))

    title_text = font.render("Game Over", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(
        center=(button_x + button_width // 2, button_y - 200 + button_height // 2)
    )
    screen.blit(title_text, title_rect)

    # Show the score under "Game Over"
    score_text = font.render(f"Your Score: {final_score}", True, (0, 0, 0))
    score_rect = score_text.get_rect(
        center=(button_x + button_width // 2, button_y - 130)
    )
    screen.blit(score_text, score_rect)

    mouse_pos = pygame.mouse.get_pos()

    # "Play Again" button
    again_rect_outer = pygame.Rect(button_x - BORDER_WIDTH, button_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0, 0, 0), again_rect_outer)
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and button_y <= mouse_pos[1] <= button_y + button_height):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR,
                         (button_x, button_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (button_x, button_y, button_width, button_height))
    button_again_text = font.render("Play Again", True, BUTTON_TEXT_COLOR)
    button_again_rect = button_again_text.get_rect(
        center=(button_x + button_width // 2, button_y + button_height // 2)
    )
    screen.blit(button_again_text, button_again_rect)

    # "Leaderboard" button
    lb_y = button_y + 100
    lb_rect_outer = pygame.Rect(button_x - BORDER_WIDTH, lb_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0, 0, 0), lb_rect_outer)
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and lb_y <= mouse_pos[1] <= lb_y + button_height):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (button_x, lb_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, lb_y, button_width, button_height))
    lb_text = font.render("Leaderboard", True, BUTTON_TEXT_COLOR)
    lb_rect = lb_text.get_rect(
        center=(button_x + button_width // 2, lb_y + button_height // 2)
    )
    screen.blit(lb_text, lb_rect)

    # "Quit" button
    quit_y = button_y + 200
    quit_rect_outer = pygame.Rect(button_x - BORDER_WIDTH, quit_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0, 0, 0), quit_rect_outer)
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and quit_y <= mouse_pos[1] <= quit_y + button_height):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (button_x, quit_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, quit_y, button_width, button_height))
    button_quit_text = font.render("Quit", True, BUTTON_TEXT_COLOR)
    button_quit_rect = button_quit_text.get_rect(
        center=(button_x + button_width // 2, quit_y + button_height // 2)
    )
    screen.blit(button_quit_text, button_quit_rect)


def handle_game_over_screen_click(events) -> str | None:
    """
    Processes clicks on the game-over screen buttons:
      - Play Again
      - Leaderboard
      - Quit
    """
    mouse_pos = pygame.mouse.get_pos()
    lb_y = button_y + 100
    quit_y = button_y + 200

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and button_y <= mouse_pos[1] <= button_y + button_height):
                return "again"

            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and lb_y <= mouse_pos[1] <= lb_y + button_height):
                return "leaderboard"

            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and quit_y <= mouse_pos[1] <= quit_y + button_height):
                return "quit"
        elif event.type == pygame.QUIT:
            return "quit"
    return None


def draw_pause_screen(screen, background, font):
    """
    Draws the pause screen with blur, 'Resume' and 'Return Home' buttons.
    """
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    title_text = font.render("Paused", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 150))
    screen.blit(title_text, title_rect)
    mouse_pos = pygame.mouse.get_pos()
    resume_rect_outer = pygame.Rect(button_x - BORDER_WIDTH, button_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0, 0, 0), resume_rect_outer)
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and button_y <= mouse_pos[1] <= button_y + button_height):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR,
                         (button_x, button_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (button_x, button_y, button_width, button_height))
    resume_text = font.render("Resume", True, BUTTON_TEXT_COLOR)
    resume_rect = resume_text.get_rect(
        center=(button_x + button_width // 2, button_y + button_height // 2)
    )
    screen.blit(resume_text, resume_rect)
    home_y = button_y + 100
    home_outer = pygame.Rect(button_x - BORDER_WIDTH, home_y - BORDER_WIDTH, button_width + BORDER_WIDTH*2, button_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0, 0, 0), home_outer)
    if (button_x <= mouse_pos[0] <= button_x + button_width
            and home_y <= mouse_pos[1] <= home_y + button_height):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR,
                         (button_x, home_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (button_x, home_y, button_width, button_height))
    home_text = font.render("Return Home", True, BUTTON_TEXT_COLOR)
    home_rect = home_text.get_rect(
        center=(button_x + button_width // 2, home_y + button_height // 2)
    )
    screen.blit(home_text, home_rect)


def handle_pause_screen_click(events) -> str | None:
    """
    Checks for clicks on the 'Resume' or 'Return Home' buttons.
    Returns 'resume' or 'home' or None.
    """
    mouse_pos = pygame.mouse.get_pos()
    home_y = button_y + 100
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and button_y <= mouse_pos[1] <= button_y + button_height):
                return "resume"
            if (button_x <= mouse_pos[0] <= button_x + button_width
                    and home_y <= mouse_pos[1] <= home_y + button_height):
                return "home"
        elif event.type == pygame.QUIT:
            return "home"
    return None


def draw_countdown_screen(screen, background, value):
    """
    Draws the countdown while resuming.
    """
    screen.blit(background, (0, 0))
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    font = pygame.font.Font("freesansbold.ttf", 80)
    text_str = str(value)

    def draw_outline_text(surface, text, font_obj, x, y):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        white = (255, 255, 255)
        black = (0, 0, 0)
        for dx, dy in offsets:
            outline_surf = font_obj.render(text, True, white)
            outline_rect = outline_surf.get_rect(center=(x + dx, y + dy))
            surface.blit(outline_surf, outline_rect)
        main_surf = font_obj.render(text, True, black)
        main_rect = main_surf.get_rect(center=(x, y))
        surface.blit(main_surf, main_rect)

    cx = screen.get_width() // 2
    cy = screen.get_height() // 2
    draw_outline_text(screen, text_str, font, cx, cy)


def draw_song_selection_screen(screen, font):
    """
    Draw the Song Selection screen.
    """
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    borderWidth = BORDER_WIDTH

    # Back button at top-left
    back_x, back_y = 20, 20
    back_w, back_h = 100, 40
    pygame.draw.rect(screen, (0, 0, 0), (back_x - borderWidth, back_y - borderWidth, back_w + borderWidth*2, back_h + borderWidth*2))
    if (back_x <= mouse_pos[0] <= back_x + back_w
            and back_y <= mouse_pos[1] <= back_y + back_h):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (back_x, back_y, back_w, back_h))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (back_x, back_y, back_w, back_h))
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_rect = back_text.get_rect(center=(back_x + back_w // 2, back_y + back_h // 2))
    screen.blit(back_text, back_rect)

    # Title in middle top
    title_text = font.render("Song Selection", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 40))
    screen.blit(title_text, title_rect)

    # Black line under title
    line_y = 70
    pygame.draw.line(screen, (0, 0, 0), (0, line_y), (screen.get_width(), line_y), 3)

    # List of songs
    start_y = line_y + 20
    spacing = 60
    for index, song_name in enumerate(SONG_OPTIONS):
        song_y = start_y + index * spacing
        song_w = 400
        song_h = 40
        song_x = (WIDTH_SCALE*AMOUNT_OF_NOTES - song_w) / 2

        pygame.draw.rect(screen, (0, 0, 0), (song_x - borderWidth, song_y - borderWidth, song_w + borderWidth*2, song_h + borderWidth*2))
        if (song_x <= mouse_pos[0] <= song_x + song_w
                and song_y <= mouse_pos[1] <= song_y + song_h):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (song_x, song_y, song_w, song_h))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (song_x, song_y, song_w, song_h))

        text_surf = font.render(song_name, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(song_x + song_w // 2, song_y + song_h // 2))
        screen.blit(text_surf, text_rect)


def handle_song_selection_screen_click(events) -> str | None:
    """
    Returns:
      "back" if the Back button is clicked,
      "song:<song_name>" if a song is clicked,
      None otherwise.
    """
    mouse_pos = pygame.mouse.get_pos()
    back_x, back_y = 20, 20
    back_w, back_h = 80, 40

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (back_x <= mouse_pos[0] <= back_x + back_w
                    and back_y <= mouse_pos[1] <= back_y + back_h):
                return "back"

            line_y = 70
            start_y = line_y + 20
            spacing = 60
            for index, song_name in enumerate(SONG_OPTIONS):
                song_x = 100
                song_y = start_y + index * spacing
                song_w = 400
                song_h = 40
                if (song_x <= mouse_pos[0] <= song_x + song_w
                        and song_y <= mouse_pos[1] <= song_y + song_h):
                    return f"song:{song_name}"

        elif event.type == pygame.QUIT:
            return "back"
    return None


def draw_leaderboard_screen(screen, font, leaderboard):
    """
    Leaderboard screen that displays top scores with a 'Back' button which takes the user to GAME_OVER.
    """
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    title_text = font.render("Leaderboard", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    # Draw up to 5 of the highest scores
    start_y = 120
    spacing = 40
    colour = (255, 255, 255)
    for i, score in enumerate(leaderboard[:5]):
        score_str = f"{i + 1}    {score}"
        score_text = font.render(score_str, True, (0, 0, 0))
        score_rect = score_text.get_rect(x=100, y=start_y + i * spacing)
        
        if colour == (255,255,255):
            colour = (200,200,200)
        else:
            colour = (255,255,255)
        pygame.draw.rect(screen, colour, (70, start_y + i*spacing - 6, screen.get_width() - 140, spacing))
        pygame.draw.line(screen, (0,0,0), (70, start_y + (i-1)*spacing - 6+spacing), (screen.get_width() - 70, start_y + (i-1)*spacing - 6+spacing), 3)
        pygame.draw.line(screen, (0,0,0), (70, start_y + i*spacing - 6+spacing), (screen.get_width() - 70, start_y + i*spacing - 6+spacing), 3)
        pygame.draw.line(screen, (0,0,0), (70, start_y + (i-1)*spacing - 6+spacing), (70, start_y + i*spacing - 6+spacing), 3)
        pygame.draw.line(screen, (0,0,0), (140, start_y + (i-1)*spacing - 6+spacing), (140, start_y + i*spacing - 6+spacing), 3)

        pygame.draw.line(screen, (0,0,0), (screen.get_width() - 70, start_y + (i-1)*spacing - 6+spacing), (screen.get_width() - 70, start_y + i*spacing - 6+spacing), 3)
        screen.blit(score_text, score_rect)

    back_x = (screen.get_width() - BUTTON_WIDTH) // 2
    back_y = 420

    pygame.draw.rect(screen, (0, 0, 0),
                     (back_x - BORDER_WIDTH, back_y - BORDER_WIDTH, BUTTON_WIDTH + BORDER_WIDTH*2, BUTTON_HEIGHT + BORDER_WIDTH*2))
    if (back_x <= mouse_pos[0] <= back_x + BUTTON_WIDTH
            and back_y <= mouse_pos[1] <= back_y + BUTTON_HEIGHT):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR,
                         (back_x, back_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR,
                         (back_x, back_y, BUTTON_WIDTH, BUTTON_HEIGHT))
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_rect = back_text.get_rect(
        center=(back_x + BUTTON_WIDTH // 2, back_y + BUTTON_HEIGHT // 2)
    )
    screen.blit(back_text, back_rect)


def handle_leaderboard_screen_click(events, screen) -> str | None:
    """
    'Back' button that takes the user to GAME_OVER.
    """
    mouse_pos = pygame.mouse.get_pos()

    back_x = (screen.get_width() - BUTTON_WIDTH) // 2
    back_y = 420

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (back_x <= mouse_pos[0] <= back_x + BUTTON_WIDTH
                    and back_y <= mouse_pos[1] <= back_y + BUTTON_HEIGHT):
                return "back"
        elif event.type == pygame.QUIT:
            return "back"
    return None

def draw_tutorial_screen(screen, font):
    """
    Tutorial screen showing players how to play the game, with a button that takes user to HOME
    """
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()
    pygame.font.init()
    fontSmall = pygame.font.Font("freesansbold.ttf", 20)

    title_text = font.render("Tutorial", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)
    line_y = 70
    pygame.draw.line(screen, (0, 0, 0), (0, line_y), (screen.get_width(), line_y), 3)

    back_x, back_y = 20, 20
    back_w, back_h = 100, 40
    pygame.draw.rect(screen, (0, 0, 0), (back_x - BORDER_WIDTH, back_y - BORDER_WIDTH, back_w + BORDER_WIDTH*2, back_h + BORDER_WIDTH*2))
    if (back_x <= mouse_pos[0] <= back_x + back_w
            and back_y <= mouse_pos[1] <= back_y + back_h):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (back_x, back_y, back_w, back_h))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (back_x, back_y, back_w, back_h))
    back_text = font.render("Back", True, BUTTON_TEXT_COLOR)
    back_rect = back_text.get_rect(center=(back_x + back_w // 2, back_y + back_h // 2))
    screen.blit(back_text, back_rect)
    pygame.draw.rect(screen, (0,0,0), (50 - BORDER_WIDTH, 120 - BORDER_WIDTH, screen.get_width() - 100 + BORDER_WIDTH*2, screen.get_height() - 170 + BORDER_WIDTH*2))
    pygame.draw.rect(screen, (200,200,200), (50, 120, screen.get_width() - 100, screen.get_height() - 170))

    back_text = fontSmall.render("Use a MIDI piano to hit a note", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 140))
    screen.blit(back_text, back_rect)

    back_text = fontSmall.render("Aim to hit a falling note within the", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 180))
    screen.blit(back_text, back_rect)
    back_text = fontSmall.render("green section", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 200))
    screen.blit(back_text, back_rect)

    back_text = fontSmall.render("Notes of different colour represent a decision,", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 240))
    screen.blit(back_text, back_rect)
    back_text = fontSmall.render("hit one note to chose path", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 260))
    screen.blit(back_text, back_rect)

    back_text = fontSmall.render("Missing a note reduces your health", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 300))
    screen.blit(back_text, back_rect)

    back_text = fontSmall.render("When health reaches zero, game is over", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 340))
    screen.blit(back_text, back_rect)

    back_text = fontSmall.render("Goal is to get as high a score as possible", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 380))
    screen.blit(back_text, back_rect)
    back_text = fontSmall.render("before you run out of health", True, (0,0,0))
    back_rect = back_text.get_rect(center=(screen.get_width()/2, 400))
    screen.blit(back_text, back_rect)

def handle_tutorial_screen_click(events) -> str | None:
    """
    Returns:
      "back" if the Back button is clicked,
      None otherwise.
    """
    mouse_pos = pygame.mouse.get_pos()
    back_x, back_y = 20, 20
    back_w, back_h = 80, 40

    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (back_x <= mouse_pos[0] <= back_x + back_w
                    and back_y <= mouse_pos[1] <= back_y + back_h):
                return "back"

        elif event.type == pygame.QUIT:
            return "back"
    return None


def draw_settings_screen(screen: pygame.Surface, font_title: pygame.font.Font) -> None:
    """
    Draws the settings screen with:
      - Back button
      - Enable Metronome (with black outline)
      - Set BPM (click to enter BPM)
      - Select MIDI Device (dropdown)
    """
    screen.fill((255, 255, 255))
    mouse_pos = pygame.mouse.get_pos()

    font_small = pygame.font.Font("freesansbold.ttf", 20)

    # BACK BUTTON
    back_x, back_y = 20, 20
    back_w, back_h = 100, 40
    pygame.draw.rect(screen, (0, 0, 0), (back_x - BORDER_WIDTH, back_y - BORDER_WIDTH, back_w + BORDER_WIDTH*2, back_h + BORDER_WIDTH*2))
    if (back_x <= mouse_pos[0] <= back_x + back_w
            and back_y <= mouse_pos[1] <= back_y + back_h):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (back_x, back_y, back_w, back_h))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (back_x, back_y, back_w, back_h))
    back_text = font_small.render("Back", True, BUTTON_TEXT_COLOR)
    back_rect = back_text.get_rect(center=(back_x + back_w // 2, back_y + back_h // 2))
    screen.blit(back_text, back_rect)

    # TITLE
    title_text = font_title.render("Settings", True, TITLE_TEXT_COLOR)
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 60))
    screen.blit(title_text, title_rect)

    start_y = 130
    spacing_y = 70

    # Enable Metronome
    metronome_y = start_y
    label_met_text = font_small.render("Enable Metronome:", True, (0, 0, 0))
    screen.blit(label_met_text, (80, metronome_y))

    # Outline
    toggle_width, toggle_height = 50, 30
    toggle_x = 300
    outline_rect = pygame.Rect(toggle_x - BORDER_WIDTH, metronome_y - BORDER_WIDTH, toggle_width + BORDER_WIDTH*2, toggle_height + BORDER_WIDTH*2)
    pygame.draw.rect(screen, (0,0,0), outline_rect)  # black outline

    # Actual toggle fill
    if ENABLE_METRONOME:
        color_toggle = BUTTON_COLOR
    else:
        color_toggle = (200, 200, 200)
    toggle_rect = pygame.Rect(toggle_x, metronome_y, toggle_width, toggle_height)
    pygame.draw.rect(screen, color_toggle, toggle_rect)

    # Set PBM
    bpm_y = metronome_y + spacing_y
    label_bpm_text = font_small.render("Set BPM:", True, (0, 0, 0))
    screen.blit(label_bpm_text, (80, bpm_y))

    # BPM input box
    input_width, input_height = 100, 40
    input_x = 300
    # Outline
    pygame.draw.rect(screen, (0,0,0), (input_x - BORDER_WIDTH, bpm_y - BORDER_WIDTH, input_width + BORDER_WIDTH*2, input_height + BORDER_WIDTH*2))
    # Fill
    if BPM_INPUT_ACTIVE:
        fill_color = (255, 255, 255)
    else:
        fill_color = (230, 230, 230)
    bpm_input_rect = pygame.Rect(input_x, bpm_y, input_width, input_height)
    pygame.draw.rect(screen, fill_color, bpm_input_rect)

    # Text in BPM box
    bpm_text_surf = font_small.render(BPM_INPUT_TEXT, True, (0, 0, 0))
    bpm_text_rect = bpm_text_surf.get_rect(center=(input_x + input_width//2, bpm_y + input_height//2))
    screen.blit(bpm_text_surf, bpm_text_rect)

    # MIDI DEVICE SELECTOR
    midi_y = bpm_y + spacing_y
    label_midi_text = font_small.render("Select MIDI Device:", True, (0, 0, 0))
    screen.blit(label_midi_text, (80, midi_y))

    # MIDI dropdown
    dropdown_width, dropdown_height = 200, 40
    dropdown_x = 300
    # Outline
    pygame.draw.rect(screen, (0,0,0), (dropdown_x - BORDER_WIDTH, midi_y - BORDER_WIDTH, dropdown_width + BORDER_WIDTH*2, dropdown_height + BORDER_WIDTH*2))
    # Fill
    pygame.draw.rect(screen, (230, 230, 230), (dropdown_x, midi_y, dropdown_width, dropdown_height))

    display_text = SELECTED_MIDI_DEVICE if SELECTED_MIDI_DEVICE else "None"
    drop_text_surf = font_small.render(display_text, True, (0, 0, 0))
    drop_text_rect = drop_text_surf.get_rect(center=(dropdown_x + dropdown_width//2, midi_y + dropdown_height//2))
    screen.blit(drop_text_surf, drop_text_rect)

    if MIDI_DROPDOWN_EXPANDED:
        # Draw a rectangle to show all the options
        for i, device_name in enumerate(MIDI_DEVICES):
            item_x = dropdown_x
            item_y = midi_y + dropdown_height + i * dropdown_height
            pygame.draw.rect(screen, (0,0,0), (item_x - BORDER_WIDTH, item_y - BORDER_WIDTH, dropdown_width + BORDER_WIDTH*2, dropdown_height + BORDER_WIDTH*2))
            # Hover effect
            if (item_x <= mouse_pos[0] <= item_x + dropdown_width
                    and item_y <= mouse_pos[1] <= item_y + dropdown_height):
                color_item = BUTTON_HOVER_COLOR
            else:
                color_item = (230, 230, 230)
            pygame.draw.rect(screen, color_item, (item_x, item_y, dropdown_width, dropdown_height))

            # Device name
            item_text_surf = font_small.render(device_name, True, (0, 0, 0))
            item_text_rect = item_text_surf.get_rect(center=(item_x + dropdown_width//2, item_y + dropdown_height//2))
            screen.blit(item_text_surf, item_text_rect)

def handle_settings_screen_click(events) -> str | None:
    """
    Handles interactions on the settings screen.
    Returns "back" if the Back button is clicked.
    Toggles metronome on the toggle button.
    Activates BPM text input on BPM box click.
    Expands or selects MIDI device if the dropdown is clicked.
    """
    import pygame
    global ENABLE_METRONOME, CURRENT_BPM, SELECTED_MIDI_DEVICE
    global MIDI_DROPDOWN_EXPANDED, BPM_INPUT_ACTIVE, BPM_INPUT_TEXT

    mouse_pos = pygame.mouse.get_pos()

    back_x, back_y = 20, 20
    back_w, back_h = 100, 40

    toggle_x, toggle_y = 300, 130
    toggle_w, toggle_h = 50, 30

    input_x, input_y = 300, 200
    input_w, input_h = 100, 40

    drop_x, drop_y = 300, 270
    drop_w, drop_h = 200, 40

    for event in events:
        if event.type == pygame.QUIT:
            return "back"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (back_x <= mouse_pos[0] <= back_x + back_w
                    and back_y <= mouse_pos[1] <= back_y + back_h):
                # On leave close dropdown and disable BPM input
                MIDI_DROPDOWN_EXPANDED = False
                BPM_INPUT_ACTIVE = False
                return "back"

            if (toggle_x <= mouse_pos[0] <= toggle_x + toggle_w
                    and toggle_y <= mouse_pos[1] <= toggle_y + toggle_h):
                ENABLE_METRONOME = not ENABLE_METRONOME

            # BPM box clicked?
            if (input_x <= mouse_pos[0] <= input_x + input_w
                    and input_y <= mouse_pos[1] <= input_y + input_h):
                BPM_INPUT_ACTIVE = True
            else:
                BPM_INPUT_ACTIVE = False
                try:
                    CURRENT_BPM = int(BPM_INPUT_TEXT)
                except ValueError:
                    pass

            # Dropdown box?
            if (drop_x <= mouse_pos[0] <= drop_x + drop_w
                    and drop_y <= mouse_pos[1] <= drop_y + drop_h):
                MIDI_DROPDOWN_EXPANDED = not MIDI_DROPDOWN_EXPANDED
            else:
                # If dropdown is expanded check if user clicked an item
                if MIDI_DROPDOWN_EXPANDED:
                    item_height = drop_h
                    for i, device_name in enumerate(MIDI_DEVICES):
                        item_y = drop_y + drop_h + i * item_height
                        if (drop_x <= mouse_pos[0] <= drop_x + drop_w
                                and item_y <= mouse_pos[1] <= item_y + item_height):
                            SELECTED_MIDI_DEVICE = device_name
                            MIDI_DROPDOWN_EXPANDED = False
                            break
                else:
                    # If user clicked outside the box
                    MIDI_DROPDOWN_EXPANDED = False

        # Keyboard events for BPM input
        if event.type == pygame.KEYDOWN and BPM_INPUT_ACTIVE:
            if event.key == pygame.K_RETURN:
                # Press Enter => finalise BPM
                BPM_INPUT_ACTIVE = False
                try:
                    CURRENT_BPM = int(BPM_INPUT_TEXT)
                except ValueError:
                    pass
            elif event.key == pygame.K_BACKSPACE:
                BPM_INPUT_TEXT = BPM_INPUT_TEXT[:-1]
            else:
                # Append the typed character if numeric
                if event.unicode.isdigit():
                    BPM_INPUT_TEXT += event.unicode

    return None
