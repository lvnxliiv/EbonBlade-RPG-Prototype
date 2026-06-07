# pause_menu.py — меню паузы

import pygame
import sys

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        btn_w, btn_h = 340, 80
        center_x = self.width // 2 - btn_w // 2

        self.buttons = {
            "resume": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/pause_resume.png", btn_w, btn_h)
            },
            "save_exit": {
                "rect": pygame.Rect(center_x, self.height // 2 + 40, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/pause_loadgame.png", btn_w, btn_h)
            },
            "exit": {
                "rect": pygame.Rect(center_x, self.height // 2 + 160, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/pause_exit.png", btn_w, btn_h)
            },
        }

        # Полупрозрачный тёмный фон для паузы
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 160))

    def _load_btn(self, path, w, h):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, btn in self.buttons.items():
                if btn["rect"].collidepoint(pos):
                    return name
        return None

    def draw(self):
        # Затемняем игру
        self.screen.blit(self.overlay, (0, 0))
        # Рисуем кнопки
        for btn in self.buttons.values():
            self.screen.blit(btn["image"], btn["rect"])