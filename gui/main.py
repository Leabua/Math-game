import sys
from pathlib import Path
import pygame

# Initialize pygame and paths before other local imports
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
from stats_manager import existing_stats, get_stats_summary


def main():
    stats = existing_stats()
    if "theme" in stats:
        set_theme(stats["theme"])

    # Use SCALED for automatic scaling while keeping high internal resolution
    flags = pygame.SCALED | pygame.RESIZABLE
    screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption("πMath")

    clock = pygame.time.Clock()

    screen = OpeningScreen(screen_surface)

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
                from stats_manager import save_stats
                save_stats(stats)

            if isinstance(screen, SetupScreen):
                if next_screen == "game":
                    game_config = {
                        "questions": screen.questions,
                        "mode": screen.mode,
                        "operation": screen.operation,
                        "level": screen.level,
                    }

            if next_screen == "theme":
                screen = ThemeScreen(pygame.display.get_surface())
            elif next_screen == "opening":
                screen = OpeningScreen(pygame.display.get_surface())
            elif next_screen == "menu":
                screen = MenuScreen(pygame.display.get_surface())
            elif next_screen == "setup":
                screen = SetupScreen(pygame.display.get_surface())
            elif next_screen == "game":
                screen = GameScreen(pygame.display.get_surface(), game_config)
            elif next_screen == "results":
                stats = existing_stats()
                summary = get_stats_summary(stats)
                game_result = {
                    "score": screen.score,
                    "total": screen.total,
                    "current_streak": stats["current_streak"],
                    "best_streak": stats["best_streak"],
                }
                screen = ResultsScreen(pygame.display.get_surface(), game_result)
            elif next_screen == "stats":
                screen = StatsScreen(pygame.display.get_surface())
            elif next_screen == "exit":
                screen = ExitScreen(pygame.display.get_surface())
            elif next_screen is None:
                running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
