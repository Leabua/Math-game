import os
from pathlib import Path

import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

BASE_WIDTH = 800
BASE_HEIGHT = 600

SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT


def sx(x):
    return int(x * SCALE_X)


def sy(y):
    return int(y * SCALE_Y)


THEMES = {
    "8008": {
        "name": "8008",
        "bg": (51, 58, 63),
        "bg_dark": (40, 46, 51),
        "fg": (242, 242, 242),
        "fg_dim": (147, 158, 161),
        "red": (244, 71, 71),
        "green": (138, 190, 183),
        "yellow": (235, 203, 139),
        "blue": (71, 170, 244),
        "purple": (173, 114, 244),
        "aqua": (138, 190, 183),
        "orange": (244, 156, 71),
        "gray": (83, 95, 101),
    },
    "bento": {
        "name": "Bento",
        "bg": (45, 54, 64),
        "bg_dark": (35, 42, 51),
        "fg": (255, 249, 230),
        "fg_dim": (100, 114, 125),
        "red": (255, 122, 122),
        "green": (187, 255, 122),
        "yellow": (255, 230, 122),
        "blue": (122, 163, 255),
        "purple": (217, 122, 255),
        "aqua": (122, 255, 255),
        "orange": (255, 176, 122),
        "gray": (72, 86, 102),
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
    "catppuccin_frappe": {
        "name": "Catppuccin Frappe",
        "bg": (48, 52, 70),
        "bg_dark": (35, 38, 52),
        "fg": (198, 208, 245),
        "fg_dim": (131, 139, 167),
        "red": (231, 130, 132),
        "green": (166, 209, 137),
        "yellow": (229, 200, 144),
        "blue": (140, 170, 238),
        "purple": (202, 158, 230),
        "aqua": (129, 200, 190),
        "orange": (239, 159, 118),
        "gray": (115, 121, 148),
    },
    "catppuccin_latte": {
        "name": "Catppuccin Latte",
        "bg": (239, 241, 245),
        "bg_dark": (220, 224, 232),
        "fg": (76, 79, 105),
        "fg_dim": (156, 160, 176),
        "red": (210, 15, 57),
        "green": (64, 160, 43),
        "yellow": (223, 142, 29),
        "blue": (30, 102, 245),
        "purple": (136, 57, 239),
        "aqua": (23, 146, 153),
        "orange": (254, 100, 11),
        "gray": (172, 176, 190),
    },
    "catppuccin_macchiato": {
        "name": "Catppuccin Macchiato",
        "bg": (36, 39, 58),
        "bg_dark": (24, 25, 38),
        "fg": (202, 211, 245),
        "fg_dim": (128, 135, 162),
        "red": (237, 135, 150),
        "green": (166, 218, 149),
        "yellow": (238, 212, 159),
        "blue": (138, 173, 244),
        "purple": (198, 160, 246),
        "aqua": (145, 215, 227),
        "orange": (245, 169, 127),
        "gray": (110, 115, 141),
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
    "everforest_dark": {
        "name": "Everforest Dark",
        "bg": (45, 53, 51),
        "bg_dark": (35, 42, 40),
        "fg": (211, 198, 170),
        "fg_dim": (122, 132, 122),
        "red": (230, 126, 128),
        "green": (167, 192, 128),
        "yellow": (219, 187, 123),
        "blue": (127, 187, 179),
        "purple": (214, 153, 182),
        "aqua": (131, 192, 146),
        "orange": (230, 152, 112),
        "gray": (133, 142, 133),
    },
    "everforest_light": {
        "name": "Everforest Light",
        "bg": (251, 245, 213),
        "bg_dark": (242, 233, 190),
        "fg": (92, 106, 102),
        "fg_dim": (147, 160, 147),
        "red": (248, 85, 81),
        "green": (141, 161, 44),
        "yellow": (223, 160, 0),
        "blue": (53, 147, 158),
        "purple": (223, 107, 117),
        "aqua": (53, 147, 158),
        "orange": (245, 125, 0),
        "gray": (147, 160, 147),
    },
    "gruvbox_dark": {
        "name": "Gruvbox Dark",
        "bg": (40, 40, 40),
        "bg_dark": (29, 32, 33),
        "fg": (235, 219, 178),
        "fg_dim": (146, 131, 116),
        "red": (204, 36, 29),
        "green": (152, 151, 26),
        "yellow": (215, 153, 33),
        "blue": (69, 133, 136),
        "purple": (177, 98, 134),
        "aqua": (104, 157, 106),
        "orange": (214, 93, 14),
        "gray": (146, 131, 116),
    },
    "gruvbox_light": {
        "name": "Gruvbox Light",
        "bg": (235, 219, 178),
        "bg_dark": (213, 196, 161),
        "fg": (60, 56, 54),
        "fg_dim": (146, 131, 116),
        "red": (204, 36, 29),
        "green": (152, 151, 26),
        "yellow": (215, 153, 33),
        "blue": (69, 133, 136),
        "purple": (177, 98, 134),
        "aqua": (104, 157, 106),
        "orange": (214, 93, 14),
        "gray": (146, 131, 116),
    },
    "laser": {
        "name": "Laser",
        "bg": (34, 5, 54),
        "bg_dark": (24, 4, 38),
        "fg": (255, 255, 255),
        "fg_dim": (181, 23, 158),
        "red": (255, 0, 0),
        "green": (0, 255, 159),
        "yellow": (254, 255, 59),
        "blue": (0, 184, 255),
        "purple": (181, 23, 158),
        "aqua": (0, 255, 255),
        "orange": (255, 112, 0),
        "gray": (114, 20, 126),
    },
    "mizu": {
        "name": "Mizu",
        "bg": (175, 206, 214),
        "bg_dark": (148, 182, 191),
        "fg": (26, 55, 61),
        "fg_dim": (91, 131, 140),
        "red": (175, 55, 55),
        "green": (55, 175, 91),
        "yellow": (175, 150, 55),
        "blue": (55, 91, 175),
        "purple": (131, 55, 175),
        "aqua": (55, 175, 175),
        "orange": (175, 91, 55),
        "gray": (91, 131, 140),
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
    "oceanic": {
        "name": "Oceanic",
        "bg": (28, 40, 51),
        "bg_dark": (21, 30, 38),
        "fg": (209, 213, 214),
        "fg_dim": (102, 115, 122),
        "red": (224, 108, 117),
        "green": (152, 195, 121),
        "yellow": (229, 192, 123),
        "blue": (97, 175, 239),
        "purple": (198, 120, 221),
        "aqua": (86, 182, 194),
        "orange": (209, 154, 102),
        "gray": (79, 91, 102),
    },
    "on_ed_dark": {
        "name": "One Dark",
        "bg": (40, 44, 52),
        "bg_dark": (33, 37, 43),
        "fg": (171, 178, 191),
        "fg_dim": (92, 99, 112),
        "red": (224, 108, 117),
        "green": (152, 195, 121),
        "yellow": (229, 192, 123),
        "blue": (97, 175, 239),
        "purple": (198, 120, 221),
        "aqua": (86, 182, 194),
        "orange": (209, 154, 102),
        "gray": (92, 99, 112),
    },
    "paper": {
        "name": "Paper",
        "bg": (238, 238, 238),
        "bg_dark": (221, 221, 221),
        "fg": (68, 68, 68),
        "fg_dim": (170, 170, 170),
        "red": (223, 51, 51),
        "green": (51, 170, 51),
        "yellow": (223, 170, 51),
        "blue": (51, 51, 223),
        "purple": (170, 51, 170),
        "aqua": (51, 170, 170),
        "orange": (223, 119, 51),
        "gray": (170, 170, 170),
    },
    "rose_pine_dark": {
        "name": "Rose Pine Dark",
        "bg": (31, 29, 46),
        "bg_dark": (25, 23, 36),
        "fg": (224, 222, 244),
        "fg_dim": (144, 140, 170),
        "red": (235, 111, 146),
        "green": (49, 175, 145),
        "yellow": (246, 193, 119),
        "blue": (156, 207, 216),
        "purple": (196, 167, 231),
        "aqua": (235, 188, 186),
        "orange": (234, 154, 151),
        "gray": (110, 106, 134),
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
    "solarized_dark": {
        "name": "Solarized Dark",
        "bg": (0, 43, 54),
        "bg_dark": (7, 54, 66),
        "fg": (131, 148, 150),
        "fg_dim": (101, 123, 131),
        "red": (220, 50, 47),
        "green": (133, 153, 0),
        "yellow": (181, 137, 0),
        "blue": (38, 139, 210),
        "purple": (108, 113, 196),
        "aqua": (42, 161, 152),
        "orange": (203, 75, 22),
        "gray": (88, 110, 117),
    },
    "solarized_light": {
        "name": "Solarized Light",
        "bg": (253, 246, 227),
        "bg_dark": (238, 232, 213),
        "fg": (101, 123, 131),
        "fg_dim": (147, 161, 161),
        "red": (220, 50, 47),
        "green": (133, 153, 0),
        "yellow": (181, 137, 0),
        "blue": (38, 139, 210),
        "purple": (108, 113, 196),
        "aqua": (42, 161, 152),
        "orange": (203, 75, 22),
        "gray": (147, 161, 161),
    },
    "synthwave": {
        "name": "Synthwave",
        "bg": (43, 35, 64),
        "bg_dark": (36, 29, 54),
        "fg": (255, 125, 255),
        "fg_dim": (114, 248, 255),
        "red": (255, 30, 104),
        "green": (114, 248, 255),
        "yellow": (255, 248, 104),
        "blue": (30, 167, 255),
        "purple": (255, 125, 255),
        "aqua": (114, 248, 255),
        "orange": (255, 140, 30),
        "gray": (73, 60, 109),
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
    "primes": "ℙ",
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
        DIFFICULTY_COLORS.update(
            {
                1: COLORS["green"],
                2: COLORS["yellow"],
                3: COLORS["orange"],
            }
        )


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
        text_color = COLORS[color] if color in COLORS else (255, 255, 255)
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
    border_width: int = 3,  # Increased from 2
    border_radius: int = 10,  # Added rounding
):
    pygame.draw.rect(
        surface, COLORS[bg_color], (x, y, width, height), border_radius=border_radius
    )
    pygame.draw.rect(
        surface,
        COLORS[border_color],
        (x, y, width, height),
        border_width,
        border_radius=border_radius,
    )


def draw_centered_box(
    surface: pygame.Surface,
    center_x: int,
    center_y: int,
    width: int,
    height: int,
    bg_color: str = "bg_dark",
    border_color: str = "fg_dim",
    border_width: int = 3,  # Increased from 2
    border_radius: int = 10,  # Added rounding
):
    x = center_x - width // 2
    y = center_y - height // 2
    draw_box(
        surface,
        x,
        y,
        width,
        height,
        bg_color,
        border_color,
        border_width,
        border_radius,
    )
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

    radius = height // 2
    pygame.draw.rect(surface, bg, (x, y, width, height), border_radius=radius)
    fill_width = int(width * min(max(progress, 0), 1))
    if fill_width > 0:
        pygame.draw.rect(surface, fill, (x, y, fill_width, height), border_radius=radius)
    pygame.draw.rect(
        surface, COLORS["fg_dim"], (x, y, width, height), 3, border_radius=radius
    )
