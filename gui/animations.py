import pygame
import random
import math
from typing import List, Tuple, Optional
from renderer import COLORS, sx, sy


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t: float) -> float:
    return 2 * t * t if t < 0.5 else 1 - (-2 * t + 2) ** 2 / 2

def ease_out_quad(t: float) -> float:
    return 1 - (1 - t) * (1 - t)

def ease_out_bounce(t: float) -> float:
    n1 = 7.5625
    d1 = 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    else:
        t -= 2.625 / d1
        return n1 * t * t + 0.984375

def ease_in_out_sine(t: float) -> float:
    return -(math.cos(math.pi * t) - 1) / 2


class Particle:
    def __init__(
        self,
        x: float,
        y: float,
        vx: float,
        vy: float,
        color: Tuple[int, int, int],
        life: int = 60,
        size: int = 4,
    ):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = sx(size)
        self.gravity = sy(0.4)
        self.drag = 0.97
        self.rotation = random.uniform(0, 360)
        self.rot_speed = random.uniform(-8, 8)
        self.shape = random.choice(["circle", "square", "diamond"])
        self.start_color = color
        self.end_color = (
            min(color[0] + 80, 255),
            min(color[1] + 80, 255),
            min(color[2] + 80, 255),
        )

    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= self.drag
        self.vy *= self.drag
        self.rotation += self.rot_speed
        self.life -= 1
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        alpha = self.life / self.max_life
        size = int(self.size * ease_out_cubic(alpha))
        if size <= 0:
            return

        r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * (1 - alpha))
        g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * (1 - alpha))
        b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * (1 - alpha))

        glow_surf = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
        glow_color = (r, g, b, int(40 * alpha))
        pygame.draw.circle(glow_surf, glow_color, (size * 3 // 2, size * 3 // 2), size * 2)
        surface.blit(glow_surf, (int(self.x) - size * 3 // 2, int(self.y) - size * 3 // 2))

        core_color = (r, g, b, int(220 * alpha))
        core_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

        if self.shape == "circle":
            pygame.draw.circle(core_surf, core_color, (size, size), size)
        elif self.shape == "square":
            rect = pygame.Rect(0, 0, size * 2, size * 2)
            pygame.draw.rect(core_surf, core_color, rect, border_radius=size // 3)
        else:
            pts = [
                (size, 0),
                (size * 2, size),
                (size, size * 2),
                (0, size),
            ]
            pygame.draw.polygon(core_surf, core_color, pts)

        rotated_core = pygame.transform.rotate(core_surf, self.rotation)
        surface.blit(rotated_core, (int(self.x) - rotated_core.get_width() // 2, int(self.y) - rotated_core.get_height() // 2))


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def emit_burst(
        self,
        x: int,
        y: int,
        count: int = 25,
        colors: List[Tuple[int, int, int]] = None,
        spread: float = 6.0,
    ):
        if colors is None:
            colors = [
                COLORS["green"],
                COLORS["yellow"],
                COLORS["aqua"],
                COLORS["orange"],
                COLORS["purple"],
            ]

        for i in range(count):
            angle = (i / count) * 2 * math.pi + random.uniform(-0.3, 0.3)
            speed = random.uniform(sx(1.5), sx(spread))
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - sy(3)
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(45, 90),
                    size=random.randint(2, 6),
                )
            )

    def emit_confetti(self, x: int, y: int, count: int = 100):
        colors = [
            COLORS["red"],
            COLORS["green"],
            COLORS["yellow"],
            COLORS["blue"],
            COLORS["purple"],
            COLORS["aqua"],
            COLORS["orange"],
        ]

        for _ in range(count):
            vx = random.uniform(-sx(6), sx(6))
            vy = random.uniform(-sy(12), -sy(3))
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(150, 220),
                    size=random.randint(3, 8),
                )
            )

    def emit_fire(self, x: int, y: int, count: int = 10):
        colors = [COLORS["orange"], COLORS["yellow"], COLORS["red"]]

        for _ in range(count):
            vx = random.uniform(-sx(2), sx(2))
            vy = random.uniform(-sy(5), -sy(1))
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(30, 60),
                    size=random.randint(2, 5),
                )
            )

    def update(self) -> bool:
        self.particles = [p for p in self.particles if p.update()]
        return len(self.particles) > 0

    def draw(self, surface: pygame.Surface):
        for particle in self.particles:
            particle.draw(surface)

    def clear(self):
        self.particles = []


class FloatingSymbol:
    def __init__(
        self,
        symbol: str,
        x: float,
        y: float,
        speed_y: float,
        color: str = "fg_dim",
        size: int = 24,
        layer: int = 0,
    ):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.base_speed_y = speed_y
        self.color = color
        self.layer = layer
        self.base_size = sx(size) * (0.5 + layer * 0.25)

        self.wobble_phase = random.uniform(0, 2 * math.pi)
        self.wobble_speed = random.uniform(0.015, 0.04)
        self.wobble_amplitude = random.uniform(0.5, 2.0)

        self.rot_speed = random.uniform(-0.5, 0.5)
        self.rotation = 0

        self.alpha = 0.0
        self.fade_in_speed = 0.02 + layer * 0.01
        self.max_alpha = 0.15 + layer * 0.15

    def update(self, screen_width: int, screen_height: int) -> bool:
        parallax = 0.5 + self.layer * 0.5
        self.y += self.base_speed_y * parallax
        self.wobble_phase += self.wobble_speed
        self.x += math.sin(self.wobble_phase) * self.wobble_amplitude
        self.rotation += self.rot_speed

        if self.alpha < self.max_alpha:
            self.alpha = min(self.max_alpha, self.alpha + self.fade_in_speed)

        return self.y < screen_height + 50 and self.x > -50 and self.x < screen_width + 50

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        text_surf = font.render(self.symbol, True, COLORS[self.color])
        current_size = int(self.base_size * ease_in_out_sine(min(1, self.alpha / self.max_alpha)))
        if current_size > 0:
            text_surf = pygame.transform.scale(
                text_surf,
                (max(1, int(text_surf.get_width() * current_size / self.base_size)),
                 max(1, int(text_surf.get_height() * current_size / self.base_size))),
            )

        if self.rotation != 0:
            text_surf = pygame.transform.rotate(text_surf, self.rotation)

        text_surf.set_alpha(int(255 * (self.alpha / self.max_alpha)))
        surface.blit(text_surf, (int(self.x), int(self.y)))


class ScreenShake:
    def __init__(self, intensity: int = 8, duration: int = 15):
        self.intensity = intensity
        self.duration = duration
        self.current_duration = 0

    def update(self) -> Tuple[int, int]:
        if self.current_duration < self.duration:
            decay = 1.0 - (self.current_duration / self.duration)
            current_intensity = int(self.intensity * decay * decay)
            offset_x = random.randint(-current_intensity, current_intensity)
            offset_y = random.randint(-current_intensity, current_intensity)
            self.current_duration += 1
            return offset_x, offset_y
        return 0, 0

    def is_active(self) -> bool:
        return self.current_duration < self.duration


class FlashEffect:
    def __init__(self, color: str, duration: int = 12):
        self.color = color
        self.duration = duration
        self.current_duration = 0

    def update(self) -> bool:
        self.current_duration += 1
        return self.current_duration < self.duration

    def get_alpha(self) -> int:
        progress = self.current_duration / self.duration
        return int(120 * (1 - progress) ** 2)

    def draw(self, surface: pygame.Surface):
        if self.current_duration < self.duration:
            flash_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            flash_surface.fill((*COLORS[self.color], self.get_alpha()))
            surface.blit(flash_surface, (0, 0))


class TransitionFade:
    def __init__(self, duration: int = 15, direction: str = "in"):
        self.duration = duration
        self.frame = 0
        self.direction = direction

    def update(self) -> bool:
        self.frame += 1
        return self.frame < self.duration

    def draw(self, surface: pygame.Surface):
        progress = self.frame / self.duration
        if self.direction == "in":
            alpha = int(255 * (1 - progress))
        else:
            alpha = int(255 * progress)

        if alpha > 0:
            overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            surface.blit(overlay, (0, 0))

    def is_done(self) -> bool:
        return self.frame >= self.duration
