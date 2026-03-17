import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import pygame
pygame.init()

from renderer import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, set_theme, get_theme, THEMES
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
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("πMath")
    
    clock = pygame.time.Clock()
    
    screen = OpeningScreen(screen)
    
    game_config = {}
    game_result = {}
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
            
            if next_screen == "setup":
                if hasattr(screen, "questions"):
                    game_config = {
                        "questions": screen.questions,
                        "mode": screen.mode,
                        "operation": screen.operation,
                        "level": screen.level,
                    }
            
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
