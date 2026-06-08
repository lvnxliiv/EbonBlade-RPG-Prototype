# pause_menu.py — меню паузы (кнопки-заглушки с русским текстом)
import pygame
import sys

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        btn_w, btn_h = 340, 80
        center_x = self.width // 2 - btn_w // 2

        # Шрифт для текста
        self.font = pygame.font.Font(None, 40)

        # Кнопки (только rect и текст, без картинок)
        self.buttons = {
            "resume": {
                "rect": pygame.Rect(center_x, self.height // 2 - 80, btn_w, btn_h),
                "text": "Продолжить"
            },
            "save_exit": {
                "rect": pygame.Rect(center_x, self.height // 2 + 40, btn_w, btn_h),
                "text": "Сохранить и выйти"
            },
            "exit": {
                "rect": pygame.Rect(center_x, self.height // 2 + 160, btn_w, btn_h),
                "text": "Выход"
            },
        }

        # Полупрозрачный фон (прозрачнее, чем раньше: альфа 100 вместо 160)
        self.overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 100))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            for name, btn in self.buttons.items():
                if btn["rect"].collidepoint(pos):
                    return name
        return None

    def draw(self):
        # Затемняем игру полупрозрачным слоем
        self.screen.blit(self.overlay, (0, 0))

        # Кнопки рисуем сами
        for btn in self.buttons.values():
            pygame.draw.rect(self.screen, (60, 60, 60), btn["rect"])
            pygame.draw.rect(self.screen, (255, 255, 255), btn["rect"], 2)

            text_surf = self.font.render(btn["text"], True, (255, 0, 0))
            text_rect = text_surf.get_rect(center=btn["rect"].center)
            self.screen.blit(text_surf, text_rect)
