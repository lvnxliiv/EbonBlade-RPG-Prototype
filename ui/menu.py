# menu.py — главное меню (кнопки-заглушки с русским текстом)
import pygame
import sys

BACKGROUND_IMAGE = "assets/ui/menu/menu_background.jpg"

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Загрузка фона (оставлено без изменений)
        bg = pygame.image.load(BACKGROUND_IMAGE).convert()
        self.background = pygame.transform.scale(bg, (self.width, self.height))

        # Параметры кнопок
        btn_w = 340
        btn_h = 75
        center_x = self.width // 2 - btn_w // 2
        spacing = 20

        # Шрифт для текста кнопок
        self.font = pygame.font.Font(None, 40)

        # Кнопки: только прямоугольники и русский текст (вместо картинок)
        self.buttons = {
            "new_game": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80, btn_w, btn_h),
                "text": "Новая игра"
            },
            "load_game": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80 + btn_h + spacing, btn_w, btn_h),
                "text": "Загрузить"
            },
            "exit": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80 + (btn_h + spacing) * 2, btn_w, btn_h),
                "text": "Выход"
            },
        }

    def handle_event(self, event):
        """Обрабатывает клик по кнопкам. Возвращает строку-действие или None."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, btn in self.buttons.items():
                if btn["rect"].collidepoint(pos):
                    return name
        return None

    def draw(self):
        # Фон (картинка)
        self.screen.blit(self.background, (0, 0))

        # Кнопки
        for btn in self.buttons.values():
            # Серый прямоугольник кнопки
            pygame.draw.rect(self.screen, (60, 60, 60), btn["rect"])
            # Белая рамка
            pygame.draw.rect(self.screen, (255, 255, 255), btn["rect"], 2)
            # Красный текст по центру
            text_surf = self.font.render(btn["text"], True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(text_surf, text_rect)
