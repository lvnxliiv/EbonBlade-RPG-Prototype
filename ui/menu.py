# menu.py — главное меню

import pygame
import sys

BACKGROUND_IMAGE = "assets/ui/menu/menu_background.jpg"

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Загрузка фона
        bg = pygame.image.load(BACKGROUND_IMAGE).convert()
        self.background = pygame.transform.scale(bg, (self.width, self.height))

        btn_w = 340
        btn_h = 75
        center_x = self.width // 2 - btn_w // 2
        spacing = 20

        self.buttons = {
            "new_game": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/button_newgame.png", btn_w, btn_h)
            },
            "load_game": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80 + btn_h + spacing, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/button_loadgame.png", btn_w, btn_h)
            },
            "exit": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80 + (btn_h + spacing) * 2, btn_w, btn_h),
                "image": self._load_btn("assets/ui/menu/button_exit.png", btn_w, btn_h)
            },
        }

    def _load_btn(self, path, w, h):
        """Загружает изображение кнопки и масштабирует"""
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (w, h))

    def handle_event(self, event):
        """Обрабатывает клик по кнопкам. Возвращает строку-действие или None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, btn in self.buttons.items():
                if btn["rect"].collidepoint(pos):
                    return name
        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for btn in self.buttons.values():
            self.screen.blit(btn["image"], btn["rect"])