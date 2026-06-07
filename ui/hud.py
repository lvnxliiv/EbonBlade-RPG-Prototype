# hud.py — интерфейс здоровья игрока

import pygame

class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.x = -5
        self.y = -10

        self.bar_full = None      # полная полоса
        self.bar_damaged = None   # повреждённая

        try:
            full_img = pygame.image.load("assets/ui/hud/healthbar_full.png").convert_alpha()
            self.bar_full = pygame.transform.scale(full_img, (335, 120))

            damaged_img = pygame.image.load("assets/ui/hud/healthbar_damaged.png").convert_alpha()
            self.bar_damaged = pygame.transform.scale(damaged_img, (335, 120))
        except Exception as e:
            print(f"[HUD] Ошибка загрузки спрайтов: {e}")

    def draw(self, player):
        # Выбираем спрайт в зависимости от здоровья
        if player.hp > 50:
            image = self.bar_full
        elif player.hp > 0:
            image = self.bar_damaged
        else:
            image = None  # смерть — healthbar исчезает

        if image:
            self.screen.blit(image, (self.x, self.y))