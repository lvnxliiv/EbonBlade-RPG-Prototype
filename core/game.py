# game.py — основной класс игры

import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS
from core.camera import Camera
from entities.player import Player
from entities.boss import Boss
from entities.boss_projectile import BossProjectile
from ui.menu import MainMenu
from ui.hud import HUD
from ui.pause_menu import PauseMenu
from ui.ending import EndingScene
from ui.victory import VictoryScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Текущее состояние игры
        self.state = "menu"

        # Интерфейсные модули
        self.main_menu = MainMenu(self.screen)
        self.hud = HUD(self.screen)
        self.pause_menu = PauseMenu(self.screen)
        self.ending_scene = EndingScene(self.screen)
        self.victory_scene = VictoryScene(self.screen)

        # Карта
        self.map_image = pygame.image.load("assets/maps/rotveil.png").convert()
        self.map_width = self.map_image.get_width()
        self.map_height = self.map_image.get_height()

        # Камера
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Игровые объекты
        self.player = Player(400, 300, scale=3.5)
        self.boss = Boss(500, 800)
        self.boss_projectiles = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state == "menu":
                action = self.main_menu.handle_event(event)
                if action == "new_game":
                    self.player = Player(400, 300, scale=3.5)
                    self.boss = Boss(500, 800)
                    self.boss_projectiles.clear()
                    self.state = "playing"
                elif action == "load_game":
                    self.player.load()
                    self.boss = Boss(500, 800)
                    self.boss_projectiles.clear()
                    self.state = "playing"
                elif action == "exit":
                    pygame.quit()
                    sys.exit()

            elif self.state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "paused"

            elif self.state == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "playing"
                action = self.pause_menu.handle_event(event)
                if action == "resume":
                    self.state = "playing"
                elif action == "save_exit":
                    self.player.save()
                    print("Игра сохранена!")
                elif action == "exit":
                    pygame.quit()
                    sys.exit()

            elif self.state == "ending":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    self.ending_scene.active = False

            elif self.state == "victory":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"
                    self.victory_scene.active = False

    def update(self):
        if self.state == "playing":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1

            self.player.update(dx, dy, self.map_width, self.map_height)
            self.camera.update(self.player.rect, self.map_width, self.map_height)

            # Атака игрока (пробел)
            if keys[pygame.K_SPACE]:
                attack_rect = self.player.attack()
                if attack_rect is not None and self.boss.alive:
                    if attack_rect.colliderect(self.boss.hitbox):
                        self.boss.take_damage(self.player.attack_damage)
                        if not self.boss.alive:
                            self.state = "victory"
                            self.victory_scene.start()

            # Босс атакует
            self.boss.update(self.player, self.boss_projectiles)

            # Обработка снарядов
            for projectile in self.boss_projectiles[:]:
                projectile.update()

                if not (0 < projectile.rect.x < self.map_width and 0 < projectile.rect.y < self.map_height):
                    self.boss_projectiles.remove(projectile)
                    continue

                if self.player.alive and self.player.hitbox.colliderect(projectile.rect):
                    self.player.take_damage(50)
                    self.boss_projectiles.remove(projectile)
                    if not self.player.alive:
                        self.state = "ending"
                        self.ending_scene.start()

        elif self.state == "ending":
            result = self.ending_scene.update()
            if result == "menu":
                self.state = "menu"
                self.ending_scene.active = False

        elif self.state == "victory":
            result = self.victory_scene.update()
            if result == "menu":
                self.state = "menu"
                self.victory_scene.active = False

    def draw(self):
        self.screen.fill((0, 0, 0))

        if self.state == "menu":
            self.main_menu.draw()

        elif self.state in ("playing", "paused"):
            map_rect = self.camera.apply(pygame.Rect(0, 0, self.map_width, self.map_height))
            self.screen.blit(self.map_image, map_rect)

            self.player.draw(self.screen, self.camera)
            self.boss.draw(self.screen, self.camera)
            for projectile in self.boss_projectiles:
                projectile.draw(self.screen, self.camera)

            self.hud.draw(self.player)

            if self.state == "paused":
                self.pause_menu.draw()

        elif self.state == "ending":
            self.ending_scene.draw()

        elif self.state == "victory":
            self.victory_scene.draw()

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()