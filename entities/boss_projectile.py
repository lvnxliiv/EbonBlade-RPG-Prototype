# boss_projectile.py — снаряд босса (ShadowSplash)

import pygame

class BossProjectile:
    def __init__(self, x, y, target_x, target_y):
        # Прямоугольник снаряда (начальная позиция и фиксированные размеры)
        self.rect = pygame.Rect(x, y, 48, 16)
        self.speed = 8  # скорость полёта в пикселях за кадр

        # Вычисляем направление к цели
        dx = target_x - x
        dy = target_y - y
        length = (dx**2 + dy**2) ** 0.5
        if length > 0:
            # Нормализуем вектор и умножаем на скорость
            self.dx = dx / length * self.speed
            self.dy = dy / length * self.speed
        else:
            self.dx = 0
            self.dy = 0

        # Загружаем спрайт снаряда
        self.image = pygame.image.load("assets/sprites/boss/ShadowSplash.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 16))

    def update(self):
        # Перемещаем снаряд по направлению
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface, camera):
        # Отрисовка с учётом камеры
        draw_rect = camera.apply(self.rect)
        surface.blit(self.image, draw_rect)