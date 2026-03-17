import os
from pathlib import Path

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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
