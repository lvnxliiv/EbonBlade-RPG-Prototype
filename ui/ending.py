# ending.py — сцена поражения (статичная, поэтапная)

import pygame

class EndingScene:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        self.active = False
        self.current_stage = 0
        self.timer = 0

        # Этапы: (кадров, ключ)
        self.stages = [
            (60,  "black"),
            (70,  "hand_left"),
            (70,  "hand_right"),
            (70,  "head"),
            (90,  "heart"),
            (70,  "shatter"),
            (160, "finish"),
        ]

        self._load_images()

    def _load_images(self):
        base = "assets/sprites/ending/"
        HAND_W, HAND_H = 480, 480
        HEAD_W, HEAD_H = 460, 460
        HRT_W,  HRT_H  = 280, 280

        def _load(path, w, h):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, (w, h))

        self.hand_left    = _load(base + "handle_left.png",  HAND_W, HAND_H)
        self.hand_right   = _load(base + "handle_right.png", HAND_W, HAND_H)
        self.head         = _load(base + "boss_head.png",     HEAD_W, HEAD_H)
        self.heart_full   = _load(base + "heart_full.png",    HRT_W,  HRT_H)
        self.heart_broken = _load(base + "heart_broken.png",  HRT_W,  HRT_H)

    def start(self):
        self.current_stage = 0
        self.timer = self.stages[0][0]
        self.active = True

    def update(self):
        if not self.active:
            return None
        self.timer -= 1
        if self.timer <= 0:
            self.current_stage += 1
            if self.current_stage >= len(self.stages):
                self.active = False
                return "menu"
            self.timer = self.stages[self.current_stage][0]
        return None

    def draw(self):
        if not self.active:
            return
        self.screen.fill((0, 0, 0))

        cx = self.width // 2
        cy = self.height // 2

        HEAD_W, HEAD_H = self.head.get_size()
        HAND_W, HAND_H = self.hand_left.get_size()
        HRT_W,  HRT_H  = self.heart_full.get_size()

        # Голова по центру, чуть выше
        head_x = cx - HEAD_W // 2
        head_y = cy - HEAD_H // 2 - 40

        overlap_x = 260
        shoulder_offset = -100
        hand_left_x  = head_x - HAND_W + overlap_x
        hand_right_x = head_x + HEAD_W - overlap_x
        hand_y = head_y - shoulder_offset

        chin_y = head_y + int(HEAD_H * 0.82)
        heart_x = cx - HRT_W // 2
        heart_y = chin_y - 20

        # Последовательное появление
        if self.current_stage >= 1:
            self.screen.blit(self.hand_left,  (hand_left_x,  hand_y))
        if self.current_stage >= 2:
            self.screen.blit(self.hand_right, (hand_right_x, hand_y))
        if self.current_stage >= 3:
            self.screen.blit(self.head, (head_x, head_y))
        if self.current_stage >= 4:
            if self.current_stage >= 5:
                self.screen.blit(self.heart_broken, (heart_x, heart_y))
            else:
                self.screen.blit(self.heart_full, (heart_x, heart_y))