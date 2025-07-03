import pygame
import random
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils import load_high_score, save_high_score, rotate_point, project, load_shapes


class PowerUp:
    def __init__(self, vertex_index, powerup_type):
        self.vertex_index = vertex_index
        self.radius = 10
        self.active = True
        self.type = powerup_type
        self.color = {
            "slow": (255, 215, 0),    # gold
            "freeze": (0, 255, 255),  # cyan
            "boost": (0, 255, 0)      # green
        }.get(powerup_type, (255, 255, 255))

    def draw(self, screen, projected_vertices):
        if self.active:
            pos = projected_vertices[self.vertex_index]
            pygame.draw.circle(screen, self.color, pos, self.radius)

    def check_collision(self, cursor_pos, projected_vertices):
        if not self.active:
            return False
        powerup_pos = projected_vertices[self.vertex_index]
        dx = powerup_pos[0] - cursor_pos[0]
        dy = powerup_pos[1] - cursor_pos[1]
        dist = (dx * dx + dy * dy) ** 0.5
        return dist < self.radius + 6


class CubeGame:
    def __init__(self, mode="classic", shape_name=None):
        pygame.init()
        pygame.mixer.init()
        pygame.joystick.init()

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(f"Cube Game - {mode.title()} Mode")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        self.mode = mode
        self.running = True

        self.angle_x = 0
        self.angle_y = 0
        self.base_rotation_speed = 0.03
        self.rotation_speed = self.base_rotation_speed
        self.score = 0
        self.level = 1
        self.best_score = load_high_score()

        self.time_limit = 30 if mode == "timed" else 60
        self.start_time = time.time()

        self.shapes = load_shapes()
        self.shape_name = shape_name or random.choice(list(self.shapes))
        shape = self.shapes[self.shape_name]
        scale_factors = {
            "cube": 2.5,
            "pyramid": 2.0,
            "octahedron": 2.0,
            "tetrahedron": 1.0,
            "hexagonal_prism": 2.0,
            "dodecahedron": 2.0,
            "icosahedron": 2.0,
            "sphere": 4.0
        }
        scale = scale_factors.get(shape_name, 1.0)
        self.vertices = [[x * scale, y * scale, z * scale] for x, y, z in shape["vertices"]]
        self.edges = shape["edges"]

        self.target_index = random.randint(1, len(self.vertices) - 1)
        self.target_visible = True
        self.last_target_move = time.time()
        self.target_move_interval = 5
        self.memory_hide_time = 2

        self.hit_flash = 0

        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

        self.power_up = None
        self.next_powerup_time = time.time() + random.randint(10, 20)
        self.powerup_active = False
        self.active_powerup_type = None
        self.powerup_end_time = 0
        self.freeze_target = False

    def get_rotated_projected_vertices(self):
        return [project(*rotate_point(*v, self.angle_x, self.angle_y)) for v in self.vertices]

    def move_target(self):
        if self.freeze_target:
            return
        if time.time() - self.last_target_move > self.target_move_interval:
            prev = self.target_index
            while self.target_index == prev:
                self.target_index = random.randint(1, len(self.vertices) - 1)
            self.last_target_move = time.time()
            self.target_visible = True

    def spawn_powerup(self):
        idx = random.randint(1, len(self.vertices) - 1)
        powerup_type = random.choice(["slow", "freeze", "boost"])
        self.power_up = PowerUp(idx, powerup_type)
        self.next_powerup_time = time.time() + random.randint(10, 20)

    def update_powerup(self, cursor_pos, projected_vertices):
        now = time.time()

        if self.powerup_active and now > self.powerup_end_time:
            if self.active_powerup_type == "slow":
                self.rotation_speed = self.base_rotation_speed
            elif self.active_powerup_type == "freeze":
                self.freeze_target = False
            self.powerup_active = False
            self.active_powerup_type = None
            self.power_up = None

        elif not self.power_up and now > self.next_powerup_time:
            self.spawn_powerup()

        elif self.power_up and self.power_up.check_collision(cursor_pos, projected_vertices):
            effect_type = self.power_up.type
            self.active_powerup_type = effect_type
            self.powerup_active = True
            self.powerup_end_time = now + 5
            self.power_up.active = False

            if effect_type == "slow":
                self.rotation_speed = self.base_rotation_speed * 0.5
            elif effect_type == "freeze":
                self.freeze_target = True
            elif effect_type == "boost":
                self.score += 10
                self.powerup_active = False
                self.power_up = None

    def draw_flash(self):
        if self.hit_flash > 0:
            overlay = pygame.Surface((800, 600))
            overlay.set_alpha(self.hit_flash)
            overlay.fill((255, 255, 255))
            self.screen.blit(overlay, (0, 0))
            self.hit_flash -= 10

    def run(self):
        while self.running:
            self.screen.fill((0, 0, 20))
            elapsed = time.time() - self.start_time
            time_left = max(0, int(self.time_limit - elapsed))

            if time_left <= 0:
                self.running = False
                save_high_score(self.score, self.best_score)
                self.show_game_over()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: self.angle_x -= self.rotation_speed
            if keys[pygame.K_s]: self.angle_x += self.rotation_speed
            if keys[pygame.K_a]: self.angle_y -= self.rotation_speed
            if keys[pygame.K_d]: self.angle_y += self.rotation_speed

            if self.joystick:
                axis_x = self.joystick.get_axis(0)
                axis_y = self.joystick.get_axis(1)
                deadzone = 0.3
                if abs(axis_x) > deadzone:
                    self.angle_y += axis_x * self.rotation_speed
                if abs(axis_y) > deadzone:
                    self.angle_x += axis_y * self.rotation_speed

            self.move_target()
            projected = self.get_rotated_projected_vertices()
            for edge in self.edges:
                pygame.draw.line(self.screen, (200, 200, 255), projected[edge[0]], projected[edge[1]], 2)

            cursor = projected[0]
            target = projected[self.target_index]

            if self.mode == "memory" and time.time() - self.last_target_move > self.memory_hide_time:
                self.target_visible = False

            if self.target_visible:
                pygame.draw.circle(self.screen, (255, 50, 50), target, 8)
            pygame.draw.circle(self.screen, (50, 255, 50), cursor, 6)

            self.update_powerup(cursor, projected)
            if self.power_up:
                self.power_up.draw(self.screen, projected)

            dist = ((cursor[0] - target[0])**2 + (cursor[1] - target[1])**2) ** 0.5
            if dist < 15:
                self.hit_flash = 100
                self.score += max(1, int(15 - dist))
                self.target_index = random.randint(1, len(self.vertices) - 1)
                self.last_target_move = time.time()
                self.target_visible = True
                if self.score % 5 == 0:
                    self.level += 1
                    self.rotation_speed += 0.005
                    self.target_move_interval = max(1.5, self.target_move_interval - 0.3)
                    if self.mode == "timed":
                        self.time_limit += 5

            self.draw_flash()
            self.draw_ui(time_left)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def draw_ui(self, time_left):
        self.screen.blit(self.font.render(f"Shape: {self.shape_name}", True, (180, 180, 255)), (10, 130))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.font.render(f"Time: {time_left}", True, (255, 255, 255)), (10, 40))
        self.screen.blit(self.font.render(f"Level: {self.level}", True, (255, 255, 255)), (10, 70))
        self.screen.blit(self.font.render(f"Best: {self.best_score}", True, (255, 215, 0)), (10, 100))
        self.screen.blit(self.font.render("Power-Ups:", True, (200, 200, 255)), (600, 10))
        self.screen.blit(self.font.render("Yellow: Slow", True, (255, 215, 0)), (600, 40))
        self.screen.blit(self.font.render("Cyan: Freeze", True, (0, 255, 255)), (600, 70))
        self.screen.blit(self.font.render("Green: +10", True, (0, 255, 0)), (600, 100))

    def show_game_over(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.font.render("Game Over", True, (255, 255, 255)), (300, 260))
        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 255, 255)), (300, 300))
        pygame.display.flip()
        pygame.time.wait(3000)
