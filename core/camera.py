# camera.py — камера, следующая за игроком

import pygame

class Camera:
    def __init__(self, width, height):
        # Создаём прямоугольник камеры, начальное положение (0,0)
        self.camera = pygame.Rect(0, 0, width, height)
        # Сохраняем размеры видимой области
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        """Смещает прямоугольник объекта на позицию камеры,
        чтобы получить координаты для отрисовки на экране."""
        # Возвращаем новый прямоугольник, сдвинутый на -camera.x, -camera.y
        return entity_rect.move(-self.camera.x, -self.camera.y)

    def update(self, target_rect, map_width, map_height):
        """Перемещает камеру так, чтобы цель была в центре,
        но камера не выходит за границы карты."""
        # Вычисляем желаемую левую границу камеры: центр цели минус полэкрана
        x = target_rect.centerx - self.width // 2
        # Желаемая верхняя граница
        y = target_rect.centery - self.height // 2

        # Ограничиваем X, чтобы камера не ушла левее 0 и не зашла за правый край
        x = max(0, min(x, map_width - self.width))
        # Аналогично для Y
        y = max(0, min(y, map_height - self.height))

        # Обновляем прямоугольник камеры
        self.camera = pygame.Rect(x, y, self.width, self.height)