# victory.py — сцена победы (вид от первого лица)
import pygame

class VictoryScene:
    def __init__(self, screen):
        # Экран, на котором будем рисовать
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Флаг активности сцены
        self.active = False
        # Номер текущего этапа (0 – первый)
        self.current_stage = 0
        # Таймер обратного отсчёта для этапа (в кадрах, 60 FPS)
        self.timer = 0

        # Список этапов: (длительность в кадрах, ключ этапа)
        self.stages = [
            (60,  "black"),         # чёрный экран
            (70,  "hand_static"),   # статичная правая рука с мечом
            (70,  "head_full"),     # целая голова босса
            (50,  "hand_swing"),    # замах руки
            (50,  "hand_return"),   # возврат руки
            (70,  "head_crack1"),   # трещина 1
            (70,  "head_crack2"),   # трещина 2
            (70,  "head_crack3"),   # разрушение
            (70,  "head_crack4"),   # полное разрушение
            (160, "finish"),        # финальная пауза
        ]

        # Загружаем все изображения
        self._load_images()

        # Текущие спрайты (меняются по ходу этапов)
        self.current_hand = None
        self.current_head = None

    def _load_images(self):
        """Загрузка спрайтов из папки assets/sprites/victory/"""
        base = "assets/sprites/victory/"

        # Желаемые размеры спрайтов (можно менять)
        HAND_W, HAND_H = 600, 600   # ширина и высота руки
        HEAD_W, HEAD_H = 500, 500   # ширина и высота головы

        # Вспомогательная функция загрузки
        def _load(path, w, h):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (w, h))

        # Загружаем три состояния руки
        self.hand_static = _load(base + "handle_right_knight.png", HAND_W, HAND_H)
        self.hand_swing  = _load(base + "handle_right_02_knight.png", HAND_W, HAND_H)
        self.hand_return = _load(base + "handle_right_03_knight.png", HAND_W, HAND_H)

        # Загружаем пять состояний головы
        self.head_full    = _load(base + "boss_head.png", HEAD_W, HEAD_H)
        self.head_crack1  = _load(base + "boss_head_02_crack.png", HEAD_W, HEAD_H)
        self.head_crack2  = _load(base + "boss_head_03_broken.png", HEAD_W, HEAD_H)
        self.head_crack3  = _load(base + "boss_head_04_heavybroken.png", HEAD_W, HEAD_H)
        self.head_crack4  = _load(base + "boss_head_05_destroyed.png", HEAD_W, HEAD_H)

    def start(self):
        """Запуск сцены с первого этапа"""
        self.current_stage = 0
        self.timer = self.stages[0][0]   # берём длительность этапа 0
        self.active = True
        self.current_hand = None
        self.current_head = None

    def update(self):
        """Обновление таймера и переход к следующему этапу.
        Возвращает 'menu', когда сцена завершена, иначе None."""
        if not self.active:
            return None

        # Отсчитываем кадры
        self.timer -= 1
        if self.timer <= 0:
            # Переход к следующему этапу
            self.current_stage += 1
            if self.current_stage >= len(self.stages):
                # Все этапы пройдены – завершаем сцену
                self.active = False
                return "menu"

            # Устанавливаем таймер для нового этапа
            self.timer = self.stages[self.current_stage][0]
            # Обновляем, какой спрайт руки/головы показывать
            self._update_sprites_for_stage()
        return None

    def _update_sprites_for_stage(self):
        """Меняет текущие спрайты в зависимости от ключа этапа"""
        stage_key = self.stages[self.current_stage][1]

        # Выбор спрайта руки
        if stage_key == "hand_static":
            self.current_hand = self.hand_static
        elif stage_key == "hand_swing":
            self.current_hand = self.hand_swing
        elif stage_key == "hand_return":
            self.current_hand = self.hand_return
        # на остальных этапах рука не меняется

        # Выбор спрайта головы
        if stage_key == "head_full":
            self.current_head = self.head_full
        elif stage_key == "head_crack1":
            self.current_head = self.head_crack1
        elif stage_key == "head_crack2":
            self.current_head = self.head_crack2
        elif stage_key == "head_crack3":
            self.current_head = self.head_crack3
        elif stage_key == "head_crack4":
            self.current_head = self.head_crack4
        # на остальных этапах голова не меняется

    def draw(self):
        """Отрисовка сцены: чёрный фон, голова, затем рука"""
        if not self.active:
            return

        # Заливаем экран чёрным
        self.screen.fill((0, 0, 0))

        # Позиция руки: правый нижний угол с отступом 20 пикселей
        hand_x = self.width - self.hand_static.get_width() - 20
        hand_y = self.height - self.hand_static.get_height() - 20

        # Позиция головы: строго по центру экрана
        head_x = self.width // 2 - self.head_full.get_width() // 2
        head_y = self.height // 2 - self.head_full.get_height() // 2

        # Рисуем сначала голову (она будет под мечом)
        if self.current_head is not None:
            self.screen.blit(self.current_head, (head_x, head_y))

        # Затем рисуем руку – меч визуально ложится на голову
        if self.current_hand is not None:
            self.screen.blit(self.current_hand, (hand_x, hand_y))