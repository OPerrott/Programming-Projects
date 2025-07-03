import pygame
import sys
import math
import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import *
from utils import rotate_point, project

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cube Game")
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

menu_rects = []
shapes_data = None
shapes = []

selected = 0
shape_rects = []
hovered_shape = None

def load_shapes(filepath="assets/shapes.json"):
    with open(filepath, "r") as f:
        return json.load(f)

def draw_text(text, y, x=400, selected=False):
    color = (255, 255, 0) if selected else (255, 255, 255)
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(x, y))
    screen.blit(rendered, rect)
    return rect

def draw_shape(surface, shape, angle_x, angle_y, center_x, center_y, scale=80, hovered=False, selected=False):
    if selected:
        color = (0, 255, 0)      # Green for selected
    elif hovered:
        color = (255, 100, 100)  # Red for hovered
    else:
        color = (100, 200, 255)  # Blue default

    vertices = [project(*rotate_point(*v, angle_x, angle_y), scale=scale * 2,
                        offset_x=center_x, offset_y=center_y)
                for v in shape["vertices"]]
    for edge in shape["edges"]:
        pygame.draw.line(surface, color, vertices[edge[0]], vertices[edge[1]], 2)

def main_menu():
    global shapes_data, shapes, hovered_shape, menu_rects, shape_rects

    # Controller setup
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    shapes_data = load_shapes()
    shapes = list(shapes_data.keys())

    options = ["Classic Mode", "Memory Mode", "Timed Rush", "Exit"]
    selecting_shape = False
    selected_mode = 0
    angle_x = angle_y = 0

    dragging = False
    drag_start_x = 0
    using_mouse = False
    controller_cooldown = 0
    selected_shape_index = 0

    while True:
        screen.fill((0, 0, 30))
        mouse_pos = pygame.mouse.get_pos()
        angle_x += 0.01
        angle_y += 0.01

        menu_rects = []
        shape_rects = []
        hovered_shape = None
        hovered_mode = None

        if controller_cooldown > 0:
            controller_cooldown -= 1

        if not selecting_shape:
            for i, option in enumerate(options):
                y = 200 + i * 60
                rect = draw_text(option, y, selected=False)
                menu_rects.append(rect)

            if using_mouse:
                for i, option in enumerate(options):
                    y = 200 + i * 60
                    draw_text(option, y, selected=(i == hovered_mode))
            else:
                for i, option in enumerate(options):
                    y = 200 + i * 60
                    draw_text(option, y, selected=(i == selected_mode))
        else:
            draw_text(f"{options[selected_mode]}", 80, x=400, selected=True)

            # Center selected shape in middle
            start_x = 400 - selected_shape_index * 180
            for i, shape_name in enumerate(shapes):
                shape_data = shapes_data[shape_name]
                center_x = start_x + i * 180
                center_y = 300

                is_selected = (i == selected_shape_index)
                is_hovered = False

                rect = pygame.Rect(center_x - 50, center_y - 50, 100, 100)
                shape_rects.append((rect, shape_name))

                if rect.collidepoint(mouse_pos):
                    is_hovered = True
                    hovered_shape = shape_name

                draw_shape(screen, shape_data, angle_x, angle_y, center_x, center_y,
                           hovered=is_hovered, selected=is_selected)

            # Draw shape name of selected shape
            if 0 <= selected_shape_index < len(shapes):
                shape_name_text = shapes[selected_shape_index]
                label = font.render(shape_name_text, True, (255, 255, 255))
                label_rect = label.get_rect(center=(400, 500))
                screen.blit(label, label_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                using_mouse = False
                if not selecting_shape:
                    if event.key in [pygame.K_DOWN, pygame.K_s]:
                        selected_mode = (selected_mode + 1) % len(options)
                    elif event.key in [pygame.K_UP, pygame.K_w]:
                        selected_mode = (selected_mode - 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        if selected_mode == len(options) - 1:
                            pygame.quit()
                            sys.exit()
                        selecting_shape = True
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_ESCAPE:
                        selecting_shape = False
                    elif event.key == pygame.K_LEFT:
                        selected_shape_index = max(0, selected_shape_index - 1)
                    elif event.key == pygame.K_RIGHT:
                        selected_shape_index = min(len(shapes) - 1, selected_shape_index + 1)
                    elif event.key == pygame.K_RETURN:
                        shape_name = shapes[selected_shape_index]
                        mode = ["classic", "memory", "timed", "stroop"][selected_mode]
                        game = CubeGame(mode=mode, shape_name=shape_name)
                        game.run()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                using_mouse = True
                if event.button == 1:
                    dragging = True
                    drag_start_x = event.pos[0]

                    if not selecting_shape:
                        for i, rect in enumerate(menu_rects):
                            if rect.collidepoint(event.pos):
                                if i == len(options) - 1:
                                    pygame.quit()
                                    sys.exit()
                                selected_mode = i
                                selecting_shape = True
                    else:
                        for i, (rect, shape_name) in enumerate(shape_rects):
                            if rect.collidepoint(event.pos):
                                selected_shape_index = i
                                shape_name = shapes[selected_shape_index]
                                mode = ["classic", "memory", "timed", "stroop"][selected_mode]
                                game = CubeGame(mode=mode, shape_name=shape_name)
                                game.run()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False

            elif event.type == pygame.MOUSEMOTION:
                if not dragging:
                    using_mouse = True

        # Controller input
        if joystick and controller_cooldown == 0:
            axis_y = joystick.get_axis(1)
            axis_x = joystick.get_axis(0)
            hat_x, hat_y = joystick.get_hat(0)

            if not selecting_shape:
                if abs(axis_y) > 0.5 or hat_y != 0:
                    selected_mode = (selected_mode + (1 if axis_y > 0 or hat_y < 0 else -1)) % len(options)
                    controller_cooldown = 10
                elif joystick.get_button(0):  # A
                    if selected_mode == len(options) - 1:
                        pygame.quit()
                        sys.exit()
                    selecting_shape = True
                    controller_cooldown = 10
            else:
                if abs(axis_x) > 0.5 or hat_x != 0:
                    delta = 1 if (axis_x > 0 or hat_x > 0) else -1
                    selected_shape_index = max(0, min(len(shapes) - 1, selected_shape_index + delta))
                    controller_cooldown = 10
                elif joystick.get_button(1):  # B
                    selecting_shape = False
                    controller_cooldown = 10
                elif joystick.get_button(0):  # A
                    if 0 <= selected_shape_index < len(shapes):
                        shape_name = shapes[selected_shape_index]
                        mode = ["classic", "memory", "timed", "stroop"][selected_mode]
                        game = CubeGame(mode=mode, shape_name=shape_name)
                        game.run()
                        controller_cooldown = 10

        clock.tick(60)

if __name__ == "__main__":
    main_menu()
