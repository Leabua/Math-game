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

        pygame.display.flip()
        clock.tick(60)

        if not screen.running:
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

            if next_screen == "theme":
                screen = ThemeScreen(pygame.display.get_surface(), sound_manager)
            elif next_screen == "opening":
                screen = OpeningScreen(pygame.display.get_surface(), sound_manager)
                sound_manager.start_music()
            elif next_screen == "menu":
                screen = MenuScreen(pygame.display.get_surface(), sound_manager)
            elif next_screen == "setup":
                screen = SetupScreen(pygame.display.get_surface(), sound_manager)
            elif next_screen == "game":
                screen = GameScreen(
                    pygame.display.get_surface(), game_config, sound_manager
                )
            elif next_screen == "results":
                stats = existing_stats()
                summary = get_stats_summary(stats)
                game_result = {
                    "score": screen.score,
                    "total": screen.total,
                    "current_streak": stats["current_streak"],
                    "best_streak": stats["best_streak"],
                }
                screen = ResultsScreen(
                    pygame.display.get_surface(), game_result, sound_manager
                )
            elif next_screen == "stats":
                screen = StatsScreen(pygame.display.get_surface(), sound_manager)
            elif next_screen == "exit":
                screen = ExitScreen(pygame.display.get_surface(), sound_manager)
            elif next_screen is None:
                sound_manager.stop_music()
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
