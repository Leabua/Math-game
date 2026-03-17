import os
from pathlib import Path

import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BASE_WIDTH = 800
BASE_HEIGHT = 600

SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT

def sx(x): return int(x * SCALE_X)
def sy(y): return int(y * SCALE_Y)

THEMES = {
    "gruvbox_light": {
        "name": "Gruvbox Light",
        "bg": (235, 219, 178),
        "bg_dark": (235, 219, 178),
        "fg": (40, 40, 40),
        "fg_dim": (102, 102, 102),
        "red": (204, 36, 29),
        "green": (152, 151, 26),
        "yellow": (215, 153, 33),
        "blue": (69, 133, 136),
        "purple": (177, 98, 134),
        "aqua": (104, 157, 106),
        "orange": (214, 93, 14),
        "gray": (168, 153, 132),
    },
    "catppuccin_mocha": {
        "name": "Catppuccin Mocha",
        "bg": (30, 30, 46),
        "bg_dark": (24, 24, 37),
        "fg": (205, 214, 244),
        "fg_dim": (134, 134, 156),
        "red": (243, 139, 168),
        "green": (166, 227, 161),
        "yellow": (249, 226, 175),
        "blue": (137, 180, 250),
        "purple": (203, 166, 247),
        "aqua": (148, 226, 213),
        "orange": (255, 158, 100),
        "gray": (92, 95, 98),
    },
    "rose_pine_dark": {
        "name": "Rose Pine Dark",
        "bg": (36, 32, 46),
        "bg_dark": (30, 26, 40),
        "fg": (224, 222, 244),
        "fg_dim": (133, 129, 153),
        "red": (235, 111, 146),
        "green": (151, 207, 148),
        "yellow": (246, 193, 119),
        "blue": (129, 176, 255),
        "purple": (199, 125, 255),
        "aqua": (130, 204, 211),
        "orange": (255, 151, 113),
        "gray": (76, 70, 86),
    },
    "tokyo_night": {
        "name": "Tokyo Night",
        "bg": (26, 26, 40),
        "bg_dark": (22, 22, 34),
        "fg": (192, 202, 245),
        "fg_dim": (95, 95, 119),
        "red": (255, 85, 85),
        "green": (121, 192, 105),
        "yellow": (255, 183, 78),
        "blue": (69, 142, 237),
        "purple": (171, 120, 255),
        "aqua": (68, 207, 208),
        "orange": (255, 125, 75),
        "gray": (68, 72, 84),
    },
    "carbon": {
        "name": "Carbon",
        "bg": (22, 22, 22),
        "bg_dark": (15, 15, 15),
        "fg": (242, 242, 242),
        "fg_dim": (102, 102, 102),
        "red": (238, 46, 49),
        "green": (57, 181, 74),
        "yellow": (246, 110, 13),
        "blue": (69, 133, 136),
        "purple": (177, 98, 134),
        "aqua": (104, 157, 106),
        "orange": (246, 110, 13),
        "gray": (102, 102, 102),
    },
    "nord": {
        "name": "Nord",
        "bg": (46, 52, 64),
        "bg_dark": (36, 41, 51),
        "fg": (216, 222, 233),
        "fg_dim": (143, 188, 187),
        "red": (191, 97, 106),
        "green": (163, 190, 140),
        "yellow": (235, 203, 139),
        "blue": (129, 161, 193),
        "purple": (180, 142, 173),
        "aqua": (136, 192, 208),
        "orange": (208, 135, 112),
        "gray": (76, 86, 106),
    },
    "serika_dark": {
        "name": "Serika Dark",
        "bg": (50, 52, 55),
        "bg_dark": (42, 43, 46),
        "fg": (209, 208, 197),
        "fg_dim": (100, 102, 105),
        "red": (202, 71, 84),
        "green": (162, 179, 28),
        "yellow": (226, 183, 20),
        "blue": (72, 142, 153),
        "purple": (187, 128, 188),
        "aqua": (148, 187, 148),
        "orange": (214, 126, 32),
        "gray": (100, 102, 105),
    },
    "dracula": {
        "name": "Dracula",
        "bg": (40, 42, 54),
        "bg_dark": (33, 34, 44),
        "fg": (248, 248, 242),
        "fg_dim": (98, 114, 164),
        "red": (255, 85, 85),
        "green": (80, 250, 123),
        "yellow": (241, 250, 140),
        "blue": (139, 233, 253),
        "purple": (189, 147, 249),
        "aqua": (139, 233, 253),
        "orange": (255, 184, 108),
        "gray": (98, 114, 164),
    },
    "cyberpunk": {
        "name": "Cyberpunk",
        "bg": (0, 8, 20),
        "bg_dark": (0, 4, 10),
        "fg": (255, 0, 153),
        "fg_dim": (0, 255, 255),
        "red": (255, 0, 85),
        "green": (0, 255, 153),
        "yellow": (255, 255, 0),
        "blue": (0, 153, 255),
        "purple": (153, 0, 255),
        "aqua": (0, 255, 255),
        "orange": (255, 153, 0),
        "gray": (0, 64, 128),
    },
}

current_theme = "gruvbox_light"

COLORS = THEMES[current_theme].copy()

DIFFICULTY_NAMES = {
    1: "Easy",
    2: "Normal",
    3: "Einstein",
}

DIFFICULTY_COLORS = {
    1: COLORS["green"],
    2: COLORS["yellow"],
    3: COLORS["orange"],
}

OPERATOR_SYMBOLS = {
    "addition": "+",
    "subtraction": "-",
    "multiplication": "×",
    "division": "÷",
}

ASSETS_DIR = Path(__file__).parent / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"

_font_cache = {}


def set_theme(theme_name: str):
    global current_theme
    if theme_name in THEMES:
        current_theme = theme_name
        COLORS.clear()
        COLORS.update(THEMES[theme_name])
        
        DIFFICULTY_COLORS.clear()
        DIFFICULTY_COLORS.update({
            1: COLORS["green"],
            2: COLORS["yellow"],
            3: COLORS["orange"],
        })


def get_theme() -> str:
    return current_theme


def get_theme_names() -> list:
    return list(THEMES.keys())


def get_font(size: int, bold: bool = False) -> pygame.font.Font:
    size = int(size * SCALE_Y)
    key = (size, bold)
    if key not in _font_cache:
        font_names = [
            "SF Pro Rounded",
            "SF Pro Display Rounded",
            "Nunito",
            "Nunito Sans",
            "Quicksand",
            "Lato",
            "Roboto",
            "segoe ui",
            "arial",
        ]
        
        font_loaded = None
        for font_name in font_names:
            try:
                font_loaded = pygame.font.SysFont(font_name, size, bold=bold)
                break
            except Exception:
                continue
        
        if font_loaded is None:
            font_loaded = pygame.font.SysFont("sans-serif", size, bold=bold)
        
        _font_cache[key] = font_loaded
    
    return _font_cache[key]


FULLSCREEN_BUTTON_RECT = (SCREEN_WIDTH - 220, 30, 190, 45)

def draw_fullscreen_button(surface: pygame.Surface, is_fullscreen: bool):
    rect = pygame.Rect(FULLSCREEN_BUTTON_RECT)
    color = "aqua" if is_fullscreen else "fg_dim"
    text = "WINDOWED" if is_fullscreen else "FULLSCREEN"
    draw_text(surface, text, rect.centerx, rect.centery, color, 18, center=True, bold=True)

def draw_text(
    surface: pygame.Surface,
    text: str,
    x: int,
    y: int,
    color="fg",
    size: int = 24,
    center: bool = False,
    bold: bool = False,
):
    font = get_font(size, bold)
    if isinstance(color, str):
        text_color = COLORS[color]
    else:
        text_color = color
    text_surface = font.render(str(text), True, text_color)
    
    if center:
        rect = text_surface.get_rect(center=(x, y))
        surface.blit(text_surface, rect)
    else:
        surface.blit(text_surface, (x, y))
    
    return text_surface.get_rect()


def draw_box(
    surface: pygame.Surface,
    x: int,
    y: int,
    width: int,
    height: int,
    bg_color: str = "bg_dark",
    border_color: str = "fg_dim",
    border_width: int = 2,
):
    pygame.draw.rect(surface, COLORS[bg_color], (x, y, width, height))
    pygame.draw.rect(surface, COLORS[border_color], (x, y, width, height), border_width)


def draw_centered_box(
    surface: pygame.Surface,
    center_x: int,
    center_y: int,
    width: int,
    height: int,
    bg_color: str = "bg_dark",
    border_color: str = "fg_dim",
    border_width: int = 2,
):
    x = center_x - width // 2
    y = center_y - height // 2
    draw_box(surface, x, y, width, height, bg_color, border_color, border_width)
    return x, y, width, height


def draw_progress_bar(
    surface: pygame.Surface,
    x: int,
    y: int,
    width: int,
    height: int,
    progress: float,
    bg_color="bg_dark",
    fill_color="green",
):
    bg = COLORS[bg_color] if isinstance(bg_color, str) else bg_color
    fill = COLORS[fill_color] if isinstance(fill_color, str) else fill_color
    
    pygame.draw.rect(surface, bg, (x, y, width, height))
    fill_width = int(width * min(max(progress, 0), 1))
    if fill_width > 0:
        pygame.draw.rect(surface, fill, (x, y, fill_width, height))
    pygame.draw.rect(surface, COLORS["fg_dim"], (x, y, width, height), 2)
