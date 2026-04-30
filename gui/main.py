import sys
from pathlib import Path
import pygame

pygame.init()
sys.path.insert(0, str(Path(__file__).parent))

from renderer import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLORS,
    set_theme,
    get_theme,
    THEMES,
)
from screens import (
    ThemeScreen,
    OpeningScreen,
    MenuScreen,
    SetupScreen,
    GameScreen,
    ResultsScreen,
    StatsScreen,
    ExitScreen,
)
from stats_manager import existing_stats, get_stats_summary, save_stats
from sound_manager import SoundManager
from animations import TransitionFade


SCREEN_MAP = {
    "theme": ThemeScreen,
    "opening": OpeningScreen,
    "menu": MenuScreen,
    "setup": SetupScreen,
    "game": GameScreen,
    "results": ResultsScreen,
    "stats": StatsScreen,
    "exit": ExitScreen,
}

SKIP_FADE_SCREENS = {"opening", "exit", None}


def main():
    stats = existing_stats()
    if "theme" in stats:
        set_theme(stats["theme"])

    sound_manager = SoundManager()
    if "sound_enabled" in stats:
        sound_manager.set_enabled(stats["sound_enabled"])

    flags = pygame.SCALED | pygame.RESIZABLE
    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption("πMath")

    clock = pygame.time.Clock()

    screen = OpeningScreen(screen_surface, sound_manager)
    transition = None

    game_config = {}
    game_result = {}
    fullscreen = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f or event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        pygame.display.set_mode(
                            (SCREEN_WIDTH, SCREEN_HEIGHT), flags | pygame.FULLSCREEN
                        )
                    else:
                        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)

                if event.key == pygame.K_q:
                    running = False

            if hasattr(screen, "handle_event"):
                screen.handle_event(event)

        if hasattr(screen, "update"):
            screen.update()

        if hasattr(screen, "draw"):
            screen.draw()

        if transition and transition.update():
            transition.draw(pygame.display.get_surface())

        pygame.display.flip()
        clock.tick(60)

        if not screen.running and transition is None:
            next_screen = getattr(screen, "next_screen", None)

            if isinstance(screen, ThemeScreen):
                set_theme(screen.selected_theme)
                stats = existing_stats()
                stats["theme"] = screen.selected_theme
                save_stats(stats)

            if isinstance(screen, MenuScreen):
                if hasattr(screen, "sound_toggle_changed"):
                    if screen.sound_toggle_changed:
                        sound_manager.set_enabled(screen.sound_enabled)
                        stats = existing_stats()
                        stats["sound_enabled"] = screen.sound_enabled
                        save_stats(stats)
                        screen.sound_toggle_changed = False

            if isinstance(screen, SetupScreen):
                if next_screen == "game":
                    game_config = {
                        "questions": screen.questions,
                        "mode": screen.mode,
                        "operation": screen.operation,
                        "level": screen.level,
                    }

            if next_screen == "results":
                stats = existing_stats()
                get_stats_summary(stats)
                game_result = {
                    "score": screen.score,
                    "total": screen.total,
                    "current_streak": stats["current_streak"],
                    "best_streak": stats["best_streak"],
                }

            if next_screen in SCREEN_MAP:
                if next_screen in SKIP_FADE_SCREENS:
                    screen = SCREEN_MAP[next_screen](pygame.display.get_surface(), sound_manager)
                    if next_screen == "opening":
                        sound_manager.start_music()
                else:
                    transition = TransitionFade(12, "out")
                    while transition and not transition.is_done():
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                        screen.draw()
                        transition.draw(pygame.display.get_surface())
                        pygame.display.flip()
                        clock.tick(60)
                        transition.update()

                    if not running:
                        break

                    screen = SCREEN_MAP[next_screen](pygame.display.get_surface(), sound_manager)
                    transition = TransitionFade(12, "in")

            elif next_screen is None:
                sound_manager.stop_music()
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
