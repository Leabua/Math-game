import pygame
import random
import math
from typing import List, Tuple
from renderer import COLORS, sx, sy


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
        self.gravity = sy(1) * 0.1

    def update(self) -> bool:
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= 1
        return self.life > 0

    def draw(self, surface: pygame.Surface):
        alpha = self.life / self.max_life
        size = int(self.size * alpha)
        if size > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def emit_burst(
        self,
        x: int,
        y: int,
        count: int = 20,
        colors: List[Tuple[int, int, int]] = None,  # type: ignore
        spread: float = 5.0,
    ):
        if colors is None:
            colors = [
                COLORS["green"],
                COLORS["yellow"],
                COLORS["aqua"],
                COLORS["orange"],
                COLORS["purple"],
            ]

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(sx(1), sx(spread))
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - sy(2)
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(40, 80),
                    size=random.randint(2, 5),
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
            vx = random.uniform(-sx(8), sx(8))
            vy = random.uniform(-sy(15), -sy(5))
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(120, 180),
                    size=random.randint(3, 8),
                )
            )

    def emit_fire(self, x: int, y: int, count: int = 10):
        colors = [COLORS["orange"], COLORS["yellow"], COLORS["red"]]

        for _ in range(count):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-3, -1)
            color = random.choice(colors)
            self.particles.append(
                Particle(
                    x,
                    y,
                    vx,
                    vy,
                    color,
                    life=random.randint(30, 60),
                    size=random.randint(2, 4),
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
    ):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.speed_y = speed_y
        self.color = color
        self.wobble = random.uniform(0, 2 * math.pi)
        self.wobble_speed = random.uniform(0.02, 0.05)

    def update(self, screen_width: int, screen_height: int) -> bool:
        self.y += self.speed_y
        self.wobble += self.wobble_speed
        self.x += math.sin(self.wobble) * 0.5
        return self.y < screen_height + 50

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        text = font.render(self.symbol, True, COLORS[self.color])
        surface.blit(text, (int(self.x), int(self.y)))


class ScreenShake:
    def __init__(self, intensity: int = 5, duration: int = 10):
        self.intensity = intensity
        self.duration = duration
        self.current_duration = 0

    def update(self) -> Tuple[int, int]:
        if self.current_duration < self.duration:
            offset_x = random.randint(-self.intensity, self.intensity)
            offset_y = random.randint(-self.intensity, self.intensity)
            self.current_duration += 1
            return offset_x, offset_y
        return 0, 0

    def is_active(self) -> bool:
        return self.current_duration < self.duration


class FlashEffect:
    def __init__(self, color: str, duration: int = 10):
        self.color = color
        self.duration = duration
        self.current_duration = 0

    def update(self) -> bool:
        self.current_duration += 1
        return self.current_duration < self.duration

    def get_alpha(self) -> int:
        progress = self.current_duration / self.duration
        return int(100 * (1 - progress))

    def draw(self, surface: pygame.Surface):
        if self.current_duration < self.duration:
            flash_surface = pygame.Surface(surface.get_size())
            flash_surface.fill(COLORS[self.color])
            flash_surface.set_alpha(self.get_alpha())
            surface.blit(flash_surface, (0, 0))
