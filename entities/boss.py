# boss.py — босс, его атаки и healthbar

import pygame
from entities.boss_projectile import BossProjectile


class Boss:
    def __init__(self, x, y, scale=3.0):
        # Базовые размеры спрайта
        self.base_width = 80
        self.base_height = 85
        self.scale = scale

        # Вычисляем реальные размеры
        w = int(self.base_width * self.scale)
        h = int(self.base_height * self.scale)
        self.rect = pygame.Rect(x, y, w, h)

        # Уменьшенный хитбокс для атаки игрока
        self.hitbox = self.rect.copy()
        self.hitbox.width = int(self.rect.width * 0.6)
        self.hitbox.height = int(self.rect.height * 0.45)
        self.hitbox.midbottom = self.rect.midbottom

        # Здоровье
        self.hp = 100
        self.max_hp = 100
        self.alive = True

        # Таймеры атаки
        self.attack_timer = 0
        self.attack_cooldown = 180               # 3 секунды
        self.attack_animation_timer = 0
        self.attack_animation_duration = 15      # кадров анимации

        # Спрайты босса
        idle_raw = pygame.image.load("assets/sprites/boss/idle_front.png").convert_alpha()
        attack_raw = pygame.image.load("assets/sprites/boss/idle_attack.png").convert_alpha()
        self.idle_image = pygame.transform.scale(idle_raw, (w, h))
        self.attack_image = pygame.transform.scale(attack_raw, (w, h))

        # Текущий отображаемый спрайт
        self.image = self.idle_image

        # Healthbar
        self.hud_full = None
        self.hud_half = None

        full_raw = pygame.image.load("assets/ui/hud/boss_healthbar.png").convert_alpha()
        hud_w = 200                                 # фиксированная ширина рамки
        hud_h = int(full_raw.get_height() * hud_w / full_raw.get_width())
        self.hud_full = pygame.transform.scale(full_raw, (hud_w, hud_h))

        half_raw = pygame.image.load("assets/ui/hud/boss_healthbar_50.png").convert_alpha()
        hud_h = int(half_raw.get_height() * hud_w / half_raw.get_width())
        self.hud_half = pygame.transform.scale(half_raw, (hud_w, hud_h))

    def take_damage(self, amount):
        """Нанести урон. При HP <= 0 босс умирает."""
        if not self.alive:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            self.alive = False

    def update(self, player, projectiles):
        """Обновление анимации и создание снарядов (только если жив)"""
        if not self.alive:
            return

        # Анимация атаки
        if self.attack_animation_timer > 0:
            self.attack_animation_timer -= 1
            if self.attack_animation_timer == 0:
                self.image = self.idle_image      # возврат в idle
        else:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_cooldown:
                self.attack_timer = 0
                self.attack_animation_timer = self.attack_animation_duration
                self.image = self.attack_image     # атакующий спрайт
                # Создаём снаряд, летящий в игрока
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery - 20,
                    player.rect.centerx,
                    player.rect.centery
                )
                projectiles.append(proj)
            else:
                self.image = self.idle_image

    def draw(self, surface, camera):
        """Отрисовка босса и подходящего healthbar'а"""
        if not self.alive:
            return

        draw_rect = camera.apply(self.rect)
        surface.blit(self.image, draw_rect)

        # Выбираем healthbar по здоровью (полный или половинный)
        if self.hud_full and self.hud_half:
            if self.hp > 50:
                hud_image = self.hud_full
            else:
                hud_image = self.hud_half

            # Позиция над головой босса по центру
            bar_x = draw_rect.centerx - hud_image.get_width() // 2
            bar_y = draw_rect.y - hud_image.get_height() - 5
            surface.blit(hud_image, (bar_x, bar_y))