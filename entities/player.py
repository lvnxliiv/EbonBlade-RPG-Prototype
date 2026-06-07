# player.py — игрок (рыцарь), движение, атака, здоровье

import pygame
import json
import os
from core.constants import PLAYER_SPEED

class Player:
    def __init__(self, x, y, scale=3.5):
        # Базовые размеры спрайта (без масштаба)
        self.base_width = 53
        self.base_height = 43
        self.scale = scale

        # Прямоугольник для отрисовки и грубых коллизий
        self.rect = pygame.Rect(
            x, y,
            int(self.base_width * self.scale),
            int(self.base_height * self.scale)
        )

        # Уменьшенный хитбокс для точных столкновений (снаряды, атака)
        self.hitbox = self.rect.copy()
        self.hitbox.width = int(self.rect.width * 0.6)
        self.hitbox.height = int(self.rect.height * 0.45)
        # Центруем хитбокс относительно низа спрайта
        self.hitbox.midbottom = self.rect.midbottom

        self.speed = PLAYER_SPEED
        self.direction = "front"  # текущее направление взгляда

        # Здоровье
        self.hp = 100
        self.max_hp = 100
        self.alive = True

        # Неуязвимость после урона (кадров)
        self.invulnerable_timer = 0
        self.invulnerable_duration = 30   # полсекунды при 60 FPS

        # --- Параметры атаки ---
        self.attack_timer = 0               # кулдаун атаки (кадров)
        self.attack_cooldown = 30           # 0.5 сек
        self.is_attacking = False           # идёт ли атака прямо сейчас
        self.attack_damage = 50             # урон за удар
        self.attack_range = 60              # дальность атаки в пикселях
        self.attack_rect = pygame.Rect(0, 0, 0, 0)  # область поражения

        # Загрузка спрайтов по четырём направлениям (без заглушек)
        self.sprites = {}
        sprite_paths = {
            "front": "assets/sprites/knight/idle_front.png",
            "back":  "assets/sprites/knight/idle_back.png",
            "left":  "assets/sprites/knight/idle_left.png",
            "right": "assets/sprites/knight/idle_right.png"
        }

        for direction, path in sprite_paths.items():
            # Вычисляем итоговый размер с учётом масштаба
            size = (int(self.base_width * self.scale), int(self.base_height * self.scale))
            # Загружаем изображение с альфа-каналом
            img = pygame.image.load(path).convert_alpha()
            # Масштабируем и сохраняем в словарь
            self.sprites[direction] = pygame.transform.scale(img, size)

    def take_damage(self, amount):
        """Получить урон с учётом неуязвимости"""
        if self.invulnerable_timer > 0 or not self.alive:
            return
        # Уменьшаем здоровье, не ниже 0
        self.hp = max(0, self.hp - amount)
        # Запускаем таймер неуязвимости
        self.invulnerable_timer = self.invulnerable_duration
        if self.hp <= 0:
            self.alive = False

    def attack(self):
        """Попытаться атаковать. Возвращает Rect атаки или None, если кулдаун."""
        if self.attack_timer > 0:
            return None  # ещё не перезарядилась
        # Запускаем кулдаун
        self.attack_timer = self.attack_cooldown
        self.is_attacking = True

        # Вычисляем прямоугольник атаки перед игроком
        if self.direction == "right":
            self.attack_rect = pygame.Rect(
                self.rect.right, self.rect.centery - 20,
                self.attack_range, 40
            )
        elif self.direction == "left":
            self.attack_rect = pygame.Rect(
                self.rect.left - self.attack_range, self.rect.centery - 20,
                self.attack_range, 40
            )
        elif self.direction == "front":
            self.attack_rect = pygame.Rect(
                self.rect.centerx - 20, self.rect.bottom,
                40, self.attack_range
            )
        else:  # back
            self.attack_rect = pygame.Rect(
                self.rect.centerx - 20, self.rect.top - self.attack_range,
                40, self.attack_range
            )
        return self.attack_rect

    def update(self, dx, dy, map_width, map_height):
        """Обновление позиции, таймеров и направления"""
        if not self.alive:
            # Если мёртв, только таймеры обновляем
            if self.invulnerable_timer > 0:
                self.invulnerable_timer -= 1
            if self.attack_timer > 0:
                self.attack_timer -= 1
            return

        # Движение
        if dx != 0 or dy != 0:
            # Нормализация вектора движения
            length = (dx**2 + dy**2) ** 0.5
            if length > 0:
                dx /= length
                dy /= length

            move_x = int(dx * self.speed)
            move_y = int(dy * self.speed)

            # Применяем смещение к rect и hitbox
            self.rect.x += move_x
            self.rect.y += move_y
            self.hitbox.x += move_x
            self.hitbox.y += move_y

            # Ограничиваем позицию границами карты
            self.rect.x = max(0, min(self.rect.x, map_width - self.rect.width))
            self.rect.y = max(0, min(self.rect.y, map_height - self.rect.height))
            # Привязываем хитбокс к низу прямоугольника
            self.hitbox.midbottom = self.rect.midbottom

            # Определяем направление взгляда по преобладающей оси
            if abs(dx) > abs(dy):
                self.direction = "right" if dx > 0 else "left"
            else:
                self.direction = "front" if dy > 0 else "back"

        # Таймеры
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.is_attacking = False

    def draw(self, surface, camera):
        """Отрисовка игрока с учётом камеры"""
        if not self.alive:
            return
        sprite = self.sprites[self.direction]
        draw_rect = camera.apply(self.rect)
        surface.blit(sprite, draw_rect)

    def save(self, filepath="saves/save.json"):
        """Сохранение состояния в файл JSON"""
        os.makedirs("saves", exist_ok=True)
        data = {
            "x": self.rect.x,
            "y": self.rect.y,
            "direction": self.direction,
            "hp": self.hp
        }
        with open(filepath, "w") as f:
            json.dump(data, f)

    def load(self, filepath="saves/save.json"):
        """Загрузка состояния из файла JSON"""
        if not os.path.exists(filepath):
            print("Файл сохранения не найден!")
            return
        with open(filepath, "r") as f:
            data = json.load(f)
        self.rect.x = data["x"]
        self.rect.y = data["y"]
        self.direction = data.get("direction", "front")
        self.hp = data.get("hp", self.max_hp)
        self.alive = self.hp > 0
        self.invulnerable_timer = 0
        self.hitbox.midbottom = self.rect.midbottom