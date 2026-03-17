import pygame
import random
import math
from typing import Optional, Callable, List, Tuple
from datetime import datetime

from renderer import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    COLORS,
    THEMES,
    DIFFICULTY_NAMES,
    DIFFICULTY_COLORS,
    OPERATOR_SYMBOLS,
    draw_text,
    draw_box,
    draw_centered_box,
    draw_progress_bar,
    get_font,
    sx,
    sy,
)
from animations import (
    ParticleSystem,
    FloatingSymbol,
    ScreenShake,
    FlashEffect,
)
from stats_manager import (
    existing_stats,
    update_stats,
    save_stats,
    get_stats_summary,
    get_chart_data,
    get_history_for_period,
)

try:
    import pygame_chart

    CHART_AVAILABLE = True
except ImportError:
    CHART_AVAILABLE = False

SYMBOLS = ["+", "-", "×", "÷", "=", "?"]

DIFFICULTY_LEVELS = {
    1: "Easy",
    2: "Normal",
    3: "Einstein",
}

GAME_MODES = {
    "1": "solve_mode",
    "2": "x_mode",
}

OPERATIONS = {
    "1": "addition",
    "2": "subtraction",
    "3": "multiplication",
    "4": "division",
}

SYMBOLS = ["+", "-", "×", "÷", "=", "?"]


class Screen:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.running = True
        self.next_screen: Optional[str] = None

    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class ThemeScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.themes = list(THEMES.keys())
        self.theme_names = [THEMES[t]["name"] for t in self.themes]

        # We start in the middle of a large list to simulate "infinite" scrolling
        # 1000 repetitions is plenty for performance while being "hard to reach bottom"
        self.repeats = 1000
        from renderer import get_theme

        current = get_theme()
        base_index = self.themes.index(current) if current in self.themes else 0

        self.selected_index = (self.repeats // 2) * len(self.themes) + base_index
        self.selected_theme = current

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index -= 1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index += 1
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                actual_index = self.selected_index % len(self.themes)
                self.selected_theme = self.themes[actual_index]
                self.next_screen = "opening"
                self.running = False
            elif event.key == pygame.K_ESCAPE:
                actual_index = self.selected_index % len(self.themes)
                self.selected_theme = self.themes[actual_index]
                self.next_screen = "opening"
                self.running = False

    def update(self):
        pass

    def draw(self):
        actual_index = self.selected_index % len(self.themes)
        preview_theme = THEMES[self.themes[actual_index]]

        self.screen.fill(preview_theme["bg"])

        fg_color = preview_theme["fg"]
        fg_dim_color = preview_theme["fg_dim"]

        title_font = get_font(48, bold=True)
        title = title_font.render("Choose Theme", True, fg_color)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, sy(100)))
        self.screen.blit(title, title_rect)

        # Draw the picker wheel
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        item_height = sy(80)

        # Show 2 above and 2 below
        for offset in range(-2, 3):
            idx = (self.selected_index + offset) % len(self.themes)
            name = self.theme_names[idx]

            # Vertical position
            y = center_y + offset * item_height

            # Styling based on distance from center
            dist = abs(offset)
            if dist == 0:
                font_size = 42
                color = fg_color
                alpha = 255
                bold = True
            elif dist == 1:
                font_size = 32
                color = fg_dim_color
                alpha = 180
                bold = False
            else:  # dist == 2
                font_size = 24
                color = fg_dim_color
                alpha = 100
                bold = False

            font = get_font(font_size, bold=bold)
            text_surf = font.render(name, True, color)
            text_surf.set_alpha(alpha)
            rect = text_surf.get_rect(center=(center_x, y))
            self.screen.blit(text_surf, rect)

            # Draw arrows for the active item
            if offset == 0:
                arrow_font = get_font(24, bold=True)
                # Reduced offset to bring them closer to the active text
                arrow_y_offset = sy(45)

                # Using geometric characters for better symmetry
                # Up arrow
                up_arrow = arrow_font.render("▲", True, fg_color)
                up_rect = up_arrow.get_rect(center=(center_x, y - arrow_y_offset))
                self.screen.blit(up_arrow, up_rect)

                # Down arrow
                down_arrow = arrow_font.render("▼", True, fg_color)
                down_rect = down_arrow.get_rect(center=(center_x, y + arrow_y_offset))
                self.screen.blit(down_arrow, down_rect)
        footer_font = get_font(16)
        footer = footer_font.render(
            "Navigate (▼▲) | Select (Enter)| Fullscreen (F) | Quit (Q)",
            True,
            fg_dim_color,
        )
        footer_rect = footer.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - sy(50))
        )
        self.screen.blit(footer, footer_rect)


class OpeningScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.frame = 0
        self.duration = 360  # Increased to 6 seconds (at 60fps)
        self.floating_symbols: List[FloatingSymbol] = []
        self.title_alpha = 0
        self.subtitle_index = 0
        self.subtitle = "Math is for everyone"
        self.subtitle_timer = 0
        self.subtitle_alpha = 255

    def update(self):
        self.frame += 1

        if self.frame < 100:
            self.title_alpha = min(255, self.title_alpha + 5)

        if self.frame > 60 and self.subtitle_index < len(self.subtitle):
            self.subtitle_timer += 1
            if self.subtitle_timer >= 3:
                self.subtitle_index += 1
                self.subtitle_timer = 0

        # Subtitle fades out at the end
        if self.frame > self.duration - 60:
            self.subtitle_alpha = max(0, self.subtitle_alpha - 5)

        if self.frame % 30 == 0:
            symbol = random.choice(SYMBOLS)
            x = random.randint(sx(50), SCREEN_WIDTH - sx(50))
            y = -sy(30)
            speed = random.uniform(sy(0.5), sy(2.0))
            color = random.choice(["fg_dim", "fg_dim", "fg_dim"])
            self.floating_symbols.append(FloatingSymbol(symbol, x, y, speed, color))

        self.floating_symbols = [
            s for s in self.floating_symbols if s.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        ]

        if self.frame >= self.duration:
            self.next_screen = "menu"
            self.running = False

    def draw(self):
        self.screen.fill(COLORS["bg"])

        # Interpolate logo position towards menu position in last 120 frames (2 seconds)
        start_y = SCREEN_HEIGHT // 2 - sy(50)
        end_y = sy(120)
        current_y = start_y

        if self.frame > self.duration - 120:
            t = (self.frame - (self.duration - 120)) / 120
            # Ease in-out quadratic
            t = 2 * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 2) / 2
            current_y = start_y + (end_y - start_y) * t

        title_font = get_font(72, bold=True)
        title = title_font.render("πMath", True, COLORS["fg"])
        title.set_alpha(self.title_alpha)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, current_y))
        self.screen.blit(title, title_rect)

        subtitle_font = get_font(24)
        partial_subtitle = self.subtitle[: self.subtitle_index]
        subtitle = subtitle_font.render(partial_subtitle, True, COLORS["fg_dim"])
        subtitle.set_alpha(self.subtitle_alpha)

        # Move subtitle with logo if it's moving
        sub_y_offset = sy(70)
        subtitle_rect = subtitle.get_rect(
            center=(SCREEN_WIDTH // 2, current_y + sub_y_offset)
        )
        self.screen.blit(subtitle, subtitle_rect)

        for symbol in self.floating_symbols:
            symbol.draw(self.screen, get_font(32))


class MenuScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.options = ["Play", "Theme", "Stats", "Quit"]
        self.selected_index = 0
        self.floating_symbols: List[FloatingSymbol] = []

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.select_option()

    def select_option(self):
        if self.selected_index == 0:
            self.next_screen = "setup"
            self.running = False
        elif self.selected_index == 1:
            self.next_screen = "theme"
            self.running = False
        elif self.selected_index == 2:
            self.next_screen = "stats"
            self.running = False
        elif self.selected_index == 3:
            self.next_screen = "exit"
            self.running = False

    def update(self):
        if random.randint(0, 20) == 0:
            symbol = random.choice(SYMBOLS)
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT)
            speed = random.uniform(0.3, 1.0) * random.choice([-1, 1])
            self.floating_symbols.append(FloatingSymbol(symbol, x, y, speed, "fg_dim"))

        self.floating_symbols = [
            s for s in self.floating_symbols if s.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        ]

    def draw(self):
        self.screen.fill(COLORS["bg"])

        for symbol in self.floating_symbols:
            symbol.draw(self.screen, get_font(28))

        title_font = get_font(64, bold=True)
        title = title_font.render("πMath", True, COLORS["fg"])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, sy(120)))
        self.screen.blit(title, title_rect)

        for i, option in enumerate(self.options):
            y = sy(250) + i * sy(70)
            color = "fg" if i == self.selected_index else "fg_dim"
            prefix = "▶ " if i == self.selected_index else "  "
            draw_text(
                self.screen,
                prefix + option,
                SCREEN_WIDTH // 2,
                y,
                color,
                32,
                center=True,
                bold=(i == self.selected_index),
            )

        draw_text(
            self.screen,
            "Navigate (▼▲) |Select (Enter)| Fullscreen (F) | Quit (Q)",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(40),
            "fg_dim",
            16,
            center=True,
        )


class SetupScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.state = "questions"
        self.input_text = ""
        self.selected_index = 0
        self.questions = 10
        self.mode = "solve_mode"
        self.operation = "addition"
        self.level = 1

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_screen = "menu"
                self.running = False

            if self.state == "questions":
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if self.input_text.isdigit() and int(self.input_text) > 0:
                        self.questions = int(self.input_text)
                        self.state = "mode"
                        self.input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                elif event.unicode.isdigit():
                    self.input_text += event.unicode

            elif self.state == "mode":
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % 2
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.mode = "solve_mode" if self.selected_index == 0 else "x_mode"
                    self.state = "operation"
                    self.selected_index = 0

            elif self.state == "operation":
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % 4
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % 4
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    ops = ["addition", "subtraction", "multiplication", "division"]
                    self.operation = ops[self.selected_index]
                    self.state = "level"
                    self.selected_index = 0

            elif self.state == "level":
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_index = (self.selected_index - 1) % 3
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_index = (self.selected_index + 1) % 3
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.level = self.selected_index + 1
                    self.next_screen = "game"
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(COLORS["bg"])

        draw_text(
            self.screen,
            "Setup Game",
            SCREEN_WIDTH // 2,
            sy(60),
            "fg",
            36,
            center=True,
            bold=True,
        )

        if self.state == "questions":
            draw_text(
                self.screen,
                "How many questions?",
                SCREEN_WIDTH // 2,
                sy(150),
                "fg",
                24,
                center=True,
            )
            draw_text(
                self.screen,
                self.input_text + "_",
                SCREEN_WIDTH // 2,
                sy(220),
                "aqua",
                48,
                center=True,
                bold=True,
            )

        elif self.state == "mode":
            draw_text(
                self.screen,
                "Choose Mode",
                SCREEN_WIDTH // 2,
                sy(150),
                "fg",
                24,
                center=True,
            )
            for i, mode in enumerate(["Solve Mode", "Find X Mode"]):
                color = "fg" if i == self.selected_index else "fg_dim"
                prefix = "▶ " if i == self.selected_index else "  "
                draw_text(
                    self.screen,
                    prefix + mode,
                    SCREEN_WIDTH // 2,
                    sy(220) + i * sy(50),
                    color,
                    24,
                    center=True,
                    bold=(i == self.selected_index),
                )

        elif self.state == "operation":
            draw_text(
                self.screen,
                "Choose Operation",
                SCREEN_WIDTH // 2,
                sy(150),
                "fg",
                24,
                center=True,
            )
            ops = [
                "Addition (+)",
                "Subtraction (-)",
                "Multiplication (×)",
                "Division (÷)",
            ]
            for i, op in enumerate(ops):
                color = "fg" if i == self.selected_index else "fg_dim"
                prefix = "▶ " if i == self.selected_index else "  "
                draw_text(
                    self.screen,
                    prefix + op,
                    SCREEN_WIDTH // 2,
                    sy(220) + i * sy(50),
                    color,
                    24,
                    center=True,
                    bold=(i == self.selected_index),
                )

        elif self.state == "level":
            draw_text(
                self.screen,
                "Choose Difficulty",
                SCREEN_WIDTH // 2,
                sy(150),
                "fg",
                24,
                center=True,
            )
            for i, level_name in enumerate(DIFFICULTY_LEVELS.values()):
                color = (
                    DIFFICULTY_COLORS[i + 1]
                    if i == self.selected_index
                    else COLORS["fg_dim"]
                )
                prefix = "▶ " if i == self.selected_index else "  "
                draw_text(
                    self.screen,
                    prefix + level_name,
                    SCREEN_WIDTH // 2,
                    sy(220) + i * sy(50),
                    color,
                    24,
                    center=True,
                    bold=(i == self.selected_index),
                )

        draw_text(
            self.screen,
            "Go back (ESC) | Fullscreen (F) | Quit (Q)",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(40),
            "fg_dim",
            16,
            center=True,
        )


class GameScreen(Screen):
    def __init__(self, screen: pygame.Surface, config: dict):
        super().__init__(screen)
        self.config = config
        self.total = config["questions"]
        self.mode = config["mode"]
        self.operation = config["operation"]
        self.level = config["level"]

        self.current_question = 0
        self.score = 0
        self.input_text = ""

        self.problem = self.generate_problem()
        self.feedback = None
        self.feedback_timer = 0

        self.particles = ParticleSystem()
        self.shake = ScreenShake(0, 0)
        self.flash = None

        self.show_answer = False
        self.correct_answer = 0

    def generate_problem(self) -> dict:
        from utilities.game_logic import generate_integer

        x = generate_integer(self.level)
        y = generate_integer(self.level)

        if self.operation == "addition":
            if self.mode == "solve_mode":
                return {"x": x, "y": y, "answer": x + y, "display": f"{x} + {y} = ?"}
            else:
                return {
                    "x": x,
                    "y": y,
                    "answer": x,
                    "display": f"x + {y} = {x + y}, x = ?",
                }

        elif self.operation == "subtraction":
            x, y = max(x, y), min(x, y)
            if self.mode == "solve_mode":
                return {"x": x, "y": y, "answer": x - y, "display": f"{x} - {y} = ?"}
            else:
                return {
                    "x": x,
                    "y": y,
                    "answer": x,
                    "display": f"x - {y} = {x - y}, x = ?",
                }

        elif self.operation == "multiplication":
            if self.mode == "solve_mode":
                return {"x": x, "y": y, "answer": x * y, "display": f"{x} × {y} = ?"}
            else:
                return {
                    "x": x,
                    "y": y,
                    "answer": x,
                    "display": f"x × {y} = {x * y}, x = ?",
                }

        elif self.operation == "division":
            factor = generate_integer(max(1, self.level - 1))
            dividend = y * factor
            if self.mode == "solve_mode":
                return {
                    "x": dividend,
                    "y": y,
                    "answer": factor,
                    "display": f"{dividend} ÷ {y} = ?",
                }
            else:
                return {
                    "x": dividend,
                    "y": y,
                    "answer": factor,
                    "display": f"x ÷ {y} = {factor}, x = ?",
                }

        return {"x": x, "y": y, "answer": x + y, "display": f"{x} + {y} = ?"}

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_screen = "menu"
                self.running = False

            if self.show_answer:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.next_question()
                return

            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.check_answer()
            elif event.key == pygame.K_MINUS:
                self.input_text += "-"
            elif event.unicode.isdigit():
                self.input_text += event.unicode

    def check_answer(self):
        if not self.input_text:
            return

        try:
            user_answer = int(self.input_text)
            if user_answer == self.problem["answer"]:
                self.score += 1
                self.particles.emit_burst(
                    SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + sy(50), 30
                )
                self.feedback = "correct"
            else:
                self.shake = ScreenShake(8, 15)
                self.flash = FlashEffect("red", 15)
                self.feedback = "wrong"
                self.correct_answer = self.problem["answer"]

            self.feedback_timer = 60
            self.show_answer = True
            self.current_question += 1

        except ValueError:
            pass

    def next_question(self):
        if self.current_question >= self.total:
            stats = existing_stats()
            stats = update_stats(
                stats, self.score, self.total, self.mode, self.operation, self.level
            )
            save_stats(stats)
            self.next_screen = "results"
            self.running = False
        else:
            self.input_text = ""
            self.problem = self.generate_problem()
            self.feedback = None
            self.show_answer = False

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer == 0 and self.show_answer:
                pass

    def draw(self):
        self.screen.fill(COLORS["bg"])

        offset_x, offset_y = self.shake.update()
        screen_copy = self.screen.copy()
        self.screen.fill(COLORS["bg"])
        self.screen.blit(screen_copy, (offset_x, offset_y))

        top_bar_y = sy(20)
        progress = (self.current_question) / self.total
        bar_height = sy(20)
        draw_progress_bar(
            self.screen,
            sx(50),
            top_bar_y,
            SCREEN_WIDTH - sx(100),
            bar_height,
            progress,
            "bg_dark",
            "green",
        )

        # Labels below the progress bar
        label_y = top_bar_y + bar_height + sy(10)

        # Question counter on the left below bar
        draw_text(
            self.screen,
            f"Question {self.current_question + 1}/{self.total}",
            sx(50),
            label_y,
            "fg_dim",
            18,
        )

        # Difficulty on the right below bar
        level_name = DIFFICULTY_NAMES[self.level]

        # Calculate width to right-align manually since renderer.draw_text doesn't support it directly
        diff_font = get_font(16)
        diff_width = diff_font.size(level_name)[0]

        draw_text(
            self.screen,
            level_name,
            SCREEN_WIDTH - sx(50) - diff_width,
            label_y,
            "fg_dim",  # Standardized to fg_dim
            16,
            center=False,
        )

        draw_text(
            self.screen,
            self.problem["display"],
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 - sy(60),
            "fg",
            48,
            center=True,
            bold=True,
        )

        input_bg_y = SCREEN_HEIGHT // 2 + sy(20)
        draw_centered_box(
            self.screen,
            SCREEN_WIDTH // 2,
            input_bg_y + sy(30),
            sx(200),
            sy(60),
            "bg_dark",
            "fg_dim",
            3,  # Updated to match new default
        )

        if self.show_answer:
            if self.feedback == "correct":
                draw_text(
                    self.screen,
                    "✓ Correct!",
                    SCREEN_WIDTH // 2,
                    input_bg_y + sy(30),
                    "green",
                    32,
                    center=True,
                    bold=True,
                )
            else:
                draw_text(
                    self.screen,
                    f"Answer: {self.correct_answer}",
                    SCREEN_WIDTH // 2,
                    input_bg_y + sy(30),
                    "red",
                    28,
                    center=True,
                    bold=True,
                )
                draw_text(
                    self.screen,
                    "Press Enter to continue",
                    SCREEN_WIDTH // 2,
                    input_bg_y + sy(70),
                    "fg_dim",
                    16,
                    center=True,
                )
        else:
            draw_text(
                self.screen,
                self.input_text + "_",
                SCREEN_WIDTH // 2,
                input_bg_y + sy(30),
                "aqua",
                36,
                center=True,
                bold=True,
            )

        draw_text(
            self.screen,
            f"Score: {self.score}",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(80),
            "yellow",
            24,
            center=True,
            bold=True,
        )

        draw_text(
            self.screen,
            "Fullscreen (F)| Quit (Q)",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(40),
            "fg_dim",
            16,
            center=True,
        )

        self.particles.update()
        self.particles.draw(self.screen)

        if self.flash and self.flash.update():
            self.flash.draw(self.screen)


class ResultsScreen(Screen):
    def __init__(self, screen: pygame.Surface, game_result: dict):
        super().__init__(screen)
        self.score = game_result["score"]
        self.total = game_result["total"]
        self.percentage = (self.score / self.total) * 100 if self.total > 0 else 0
        self.is_perfect = self.percentage == 100
        self.current_streak = game_result.get("current_streak", 0)
        self.best_streak = game_result.get("best_streak", 0)

        self.particles = ParticleSystem()
        if self.is_perfect:
            for _ in range(5):
                self.particles.emit_confetti(SCREEN_WIDTH // 2, 0, 30)

        self.show_confetti = self.is_perfect
        self.options = ["Play Again", "Menu", "Stats"]
        self.selected_index = 0

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_screen = "menu"
                self.running = False
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.selected_index = (self.selected_index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self.selected_index == 0:
                    self.next_screen = "setup"
                elif self.selected_index == 1:
                    self.next_screen = "menu"
                elif self.selected_index == 2:
                    self.next_screen = "stats"
                self.running = False

    def update(self):
        if self.show_confetti:
            if random.randint(0, 3) == 0:
                self.particles.emit_confetti(random.randint(0, SCREEN_WIDTH), -20, 5)
            self.particles.update()
            self.particles.draw(self.screen)

    def draw(self):
        self.screen.fill(COLORS["bg"])

        if self.show_confetti:
            self.particles.draw(self.screen)

        if self.is_perfect:
            draw_text(
                self.screen,
                "🎉 PERFECT! 🎉",
                SCREEN_WIDTH // 2,
                sy(80),
                "yellow",
                48,
                center=True,
                bold=True,
            )

        draw_text(
            self.screen,
            f"{self.score}/{self.total}",
            SCREEN_WIDTH // 2,
            sy(160),
            "fg",
            64,
            center=True,
            bold=True,
        )

        draw_text(
            self.screen,
            f"{self.percentage:.0f}%",
            SCREEN_WIDTH // 2,
            sy(230),
            "aqua",
            36,
            center=True,
        )

        if self.current_streak > 0:
            draw_text(
                self.screen,
                f"🔥 {self.current_streak} streak!",
                SCREEN_WIDTH // 2,
                sy(290),
                "orange",
                24,
                center=True,
            )

        for i, option in enumerate(self.options):
            y = sy(380) + i * sy(60)
            color = "fg" if i == self.selected_index else "fg_dim"
            prefix = "▶ " if i == self.selected_index else "  "
            draw_text(
                self.screen,
                prefix + option,
                SCREEN_WIDTH // 2,
                y,
                color,
                24,
                center=True,
                bold=(i == self.selected_index),
            )

        draw_text(
            self.screen,
            "Go back (ESC) | Fullscreen (F) | Quit (Q)",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(40),
            "fg_dim",
            16,
            center=True,
        )


class StatsScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.period = "all"
        self.period_options = ["today", "week", "all"]
        self.period_labels = {"today": "Today", "week": "This Week", "all": "All Time"}
        self.selected_period_index = 2
        self.stats = existing_stats()
        self.summary = get_stats_summary(self.stats)
        self.chart_data = get_chart_data(self.stats, self.period)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_screen = "menu"
                self.running = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_period_index = (self.selected_period_index - 1) % len(
                    self.period_options
                )
                self.update_period()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_period_index = (self.selected_period_index + 1) % len(
                    self.period_options
                )
                self.update_period()

    def update_period(self):
        self.period = self.period_options[self.selected_period_index]
        self.chart_data = get_chart_data(self.stats, self.period)

    def update(self):
        self.stats = existing_stats()
        self.summary = get_stats_summary(self.stats)
        self.chart_data = get_chart_data(self.stats, self.period)

    def draw(self):
        self.screen.fill(COLORS["bg"])

        draw_text(
            self.screen,
            "Statistics",
            SCREEN_WIDTH // 2,
            30,
            "fg",
            32,
            center=True,
            bold=True,
        )

        for i, period in enumerate(self.period_options):
            x = sx(200) + i * sx(150)
            color = "fg" if i == self.selected_period_index else "fg_dim"
            draw_text(
                self.screen,
                self.period_labels[period],
                x,
                sy(75),
                color,
                18,
                center=True,
                bold=(i == self.selected_period_index),
            )

        y_offset = sy(120)

        draw_text(
            self.screen,
            f"Games Played: {self.summary['games_played']}",
            sx(80),
            y_offset,
            "fg",
            20,
        )
        draw_text(
            self.screen,
            f"Total Questions: {self.summary['total_questions']}",
            sx(80),
            y_offset + sy(30),
            "fg",
            20,
        )
        draw_text(
            self.screen,
            f"Accuracy: {self.summary['overall_accuracy']:.1f}%",
            sx(80),
            y_offset + sy(60),
            "aqua",
            20,
        )
        draw_text(
            self.screen,
            f"Best Score: {self.summary['best_score_percent']:.1f}%",
            sx(80),
            y_offset + sy(90),
            "yellow",
            20,
        )
        draw_text(
            self.screen,
            f"Best Streak: {self.summary['best_streak']}",
            sx(80),
            y_offset + sy(120),
            "orange",
            20,
        )

        if CHART_AVAILABLE and self.chart_data["sessions"]:
            chart_x, chart_y = sx(380), sy(120)
            chart_w, chart_h = sx(380), sy(200)

            draw_box(
                self.screen, chart_x, chart_y, chart_w, chart_h, "bg_dark", "fg_dim", 1
            )

            try:
                fig = pygame_chart.Figure(
                    self.screen,
                    chart_x,
                    chart_y,
                    chart_w,
                    chart_h,
                    bg_color=COLORS["bg_dark"],
                )

                if len(self.chart_data["sessions"]) > 0:
                    fig.line(
                        "accuracy",
                        self.chart_data["sessions"],
                        self.chart_data["accuracy"],
                        color=COLORS["aqua"],
                    )

                fig.set_title("Accuracy %", color=COLORS["fg"], font_size=14)
                fig.set_xlabel("Session", color=COLORS["fg_dim"], font_size=10)
                fig.set_ylabel("%", color=COLORS["fg_dim"], font_size=10)
                fig.draw()
            except Exception as e:
                draw_text(
                    self.screen,
                    "Chart unavailable",
                    chart_x + chart_w // 2,
                    chart_y + chart_h // 2,
                    "fg_dim",
                    16,
                    center=True,
                )
        else:
            draw_text(
                self.screen,
                "No data for this period",
                SCREEN_WIDTH // 2,
                sy(250),
                "fg_dim",
                20,
                center=True,
            )

        if CHART_AVAILABLE and self.chart_data["sessions"]:
            bar_x, bar_y = sx(80), sy(350)
            bar_w, bar_h = sx(300), sy(150)
            draw_box(self.screen, bar_x, bar_y, bar_w, bar_h, "bg_dark", "fg_dim", 1)

            try:
                fig2 = pygame_chart.Figure(
                    self.screen,
                    bar_x,
                    bar_y,
                    bar_w,
                    bar_h,
                    bg_color=COLORS["bg_dark"],
                )

                fig2.bar(
                    "questions",
                    self.chart_data["sessions"],
                    self.chart_data["questions"],
                    color=COLORS["blue"],
                )

                fig2.set_title(
                    "Questions per Session", color=COLORS["fg"], font_size=14
                )
                fig2.draw()
            except:
                pass

        draw_text(
            self.screen,
            "← → to change period | ESC to go back | F for Fullscreen | Q to Quit",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - sy(40),
            "fg_dim",
            16,
            center=True,
        )


class ExitScreen(Screen):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.frame = 0
        self.duration = 120
        self.floating_symbols: List[FloatingSymbol] = []
        self.alpha = 255

    def update(self):
        self.frame += 1

        if random.randint(0, 10) == 0:
            symbol = random.choice(SYMBOLS)
            x = random.randint(sx(50), SCREEN_WIDTH - sx(50))
            y = SCREEN_HEIGHT + sy(30)
            speed = random.uniform(-sy(2), -sy(0.5))
            self.floating_symbols.append(FloatingSymbol(symbol, x, y, speed, "fg_dim"))

        self.floating_symbols = [
            s for s in self.floating_symbols if s.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        ]

        if self.frame > self.duration - 30:
            self.alpha = max(0, self.alpha - 10)

        if self.frame >= self.duration:
            self.running = False

    def draw(self):
        self.screen.fill(COLORS["bg"])

        for symbol in self.floating_symbols:
            symbol.draw(self.screen, get_font(28))

        if self.alpha > 0:
            title_font = get_font(48, bold=True)
            title = title_font.render("Thanks for Playing!", True, COLORS["fg"])
            title.set_alpha(self.alpha)
            title_rect = title.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - sy(30))
            )
            self.screen.blit(title, title_rect)

            draw_text(
                self.screen,
                "Come back soon!",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + sy(30),
                "fg_dim",
                24,
                center=True,
            )
