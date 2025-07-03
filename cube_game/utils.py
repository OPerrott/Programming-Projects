import os
import math
import json


def load_high_score(path="assets/highscore.txt"):
    if os.path.exists(path):
        with open(path, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0
    return 0


def save_high_score(score, best, path="assets/highscore.txt"):
    if score > best:
        with open(path, "w") as f:
            f.write(str(score))


def rotate_point(x, y, z, angle_x, angle_y):
    xz = x * math.cos(angle_y) - z * math.sin(angle_y)
    zz = x * math.sin(angle_y) + z * math.cos(angle_y)
    yz = y * math.cos(angle_x) - zz * math.sin(angle_x)
    zz = y * math.sin(angle_x) + zz * math.cos(angle_x)
    return xz, yz, zz


def project(x, y, z, scale=100, offset_x=400, offset_y=300):
    factor = scale / (z + 5)
    screen_x = int(x * factor + offset_x)
    screen_y = int(y * factor + offset_y)
    return screen_x, screen_y



def load_shapes(filepath="assets/shapes.json"):
    with open(filepath, "r") as f:
        return json.load(f)