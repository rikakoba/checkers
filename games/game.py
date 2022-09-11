import sys
import time
import pygame
import random

from config import *
from checkers import *

display = pygame.display.set_mode((width, height))
fields = []
pos = [
    ["-", "b", "-", "b", "-", "b", "-", "b"],
    ["b", "-", "b", "-", "b", "-", "b", "-"],
    ["-", "b", "-", "b", "-", "b", "-", "b"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["-", "-", "-", "-", "-", "-", "-", "-"],
    ["r", "-", "r", "-", "r", "-", "r", "-"],
    ["-", "r", "-", "r", "-", "r", "-", "r"],
    ["r", "-", "r", "-", "r", "-", "r", "-"]
]
current_checker = []
possible_direction = []
kill_direction = []
img = {
    "b": pygame.transform.scale(pygame.image.load("images/checkers-checker-black.png"), (field_size, field_size)),
    "r": pygame.transform.scale(pygame.image.load("images/checkers-checker-red.png"), (field_size, field_size)),
    "rk": pygame.transform.scale(pygame.image.load("images/checkers-checker-red-king.png"), (field_size, field_size)),
    "bk": pygame.transform.scale(pygame.image.load("images/checkers-checker-black-king.png"), (field_size, field_size))
}
checkers_red = []
checkers_black = []
player = True


def create_checkers():
    for i in range(8):
        for g in range(8):
            if pos[i][g] == "r":
                checkers_red.append(Checker(i, g, "b"))
            elif pos[i][g] == "b":
                checkers_black.append(Checker(i, g, "r"))


def show_checkers():
    for x, i in enumerate(pos):
        for y, g in enumerate(i):
            if g != "-":
                display.blit(img[g], fields[x][y])


def show_field():
    for i in range(8):
        for g in range(8):
            color = (255, 255, 255)
            if (i + g) % 2 == 1:
                color = (200, 200, 200)
            pygame.draw.rect(display, color, fields[i][g])


def set_field():
    for i in range(8):
        line = []
        for g in range(8):
            line.append(pygame.Rect(g * field_size, i * field_size, field_size, field_size))
        fields.append(line)


def change(checker):
    pos[checker.i][checker.g] = "bk" if checker.enemy == "r" else "rk"
    if checker.enemy == "r":
        checkers_black.append(Checker_king(checker.i, checker.g, checker.enemy))
        checkers_black.remove(checker)
    else:
        checkers_red.append(Checker_king(checker.i, checker.g, checker.enemy))
        checkers_red.remove(checker)


def check_events():
    global player
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            g = int(x / field_size)
            i = int(y / field_size)
            if current_checker:
                for p in kill_direction:
                    if p[0] == i and p[1] == g:
                        for po in current_checker[0].dict_kill[p]:
                            pos[po[0]][po[1]] = "-"
                            for e in checkers_black:
                                if e.i == po[0] and e.g == po[1]:
                                    checkers_black.remove(e)
                        current_checker[0].move(pos, i, g)
                        if current_checker[0].i == 0:
                            change(current_checker[0])
                        possible_direction.clear()
                        kill_direction.clear()
                        current_checker.clear()
                        player = False
                        return
                for p in possible_direction:
                    if p[0] == i and p[1] == g:
                        current_checker[0].move(pos, i, g)
                        if current_checker[0].i == 0:
                            change(current_checker[0])
                        current_checker.clear()
                        possible_direction.clear()
                        kill_direction.clear()
                        player = False
                        return
            if player:
                for ch in checkers_red:
                    if ch.i == i and ch.g == g:
                        current_checker.clear()
                        possible_direction.clear()
                        kill_direction.clear()
                        current_checker.append(ch)
                        ch.check(pos)
                        for p in ch.dict_kill:
                            kill_direction.append(p)
                        for p in ch.kill:
                            kill_direction.append(p)
                        if not kill_direction:
                            for p in ch.pos:
                                possible_direction.append(p)
                        break
                else:
                    possible_direction.clear()
                    current_checker.clear()
                    kill_direction.clear()


def show_kill():
    for i in kill_direction:
        pygame.draw.rect(display, "red", (i[1] * field_size, i[0] * field_size, field_size, field_size), border_radius=field_size // 2)


def show_possible():
    for i in possible_direction:
        pygame.draw.rect(display, "green", (i[1] * field_size, i[0] * field_size, field_size, field_size), border_radius=field_size // 2)


def update_screen():
    display.fill("white")
    show_field()
    show_possible()
    show_kill()
    show_checkers()
    pygame.display.update()


def move_black():
    black = []
    kill = []
    global player
    for i in checkers_black:
        i.check(pos)
        if i.kill:
            kill.append(i)
        if i.pos:
            black.append(i)
        if i.dict_kill:
            kill.append(i)
    if kill:
        r = random.choice(kill)
        d = random.choice(list(r.dict_kill.keys()))
        time.sleep(1)
        for po in r.dict_kill[d]:
            pos[po[0]][po[1]] = "-"
            for k in checkers_red:
                if k.i == po[0] and k.g == po[1]:
                    checkers_red.remove(k)
        r.move(pos, d[0], d[1])
        if r.i == 7:
            change(r)
    elif black:
        r = random.choice(black)
        d = random.choice(r.pos)
        time.sleep(1)
        r.move(pos, d[0], d[1])
        if r.i == 7:
            change(r)
    player = True


def main():
    set_field()
    create_checkers()
    while True:
        if not player:
            move_black()
        check_events()
        update_screen()


main()