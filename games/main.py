import sys
import pygame
import random

height = 600
width = 800
min_size = min(height, width)
field_img = pygame.image.load("images/field.jpg")
field_rect = field_img.get_rect()
checkers_red_img = pygame.image.load("images/checkers-checker-red.png")
checkers_black_img = pygame.image.load("images/checkers-checker-black.png")
high_light_yellow = pygame.image.load("images/checkers-highlight-yellow.png")
high_light_red = pygame.image.load("images/checkers-highlight-red.png")
high_light_red = pygame.transform.scale(high_light_red, (checkers_red_img.get_rect().width + 7, checkers_red_img.get_rect().height + 7))
high_light_white = pygame.image.load("images/checkers-highlight-white.png")
high_light_yellow = pygame.transform.scale(high_light_yellow, (checkers_red_img.get_rect().width + 7, checkers_red_img.get_rect().height + 7))
high_light_green = pygame.image.load("images/checkers-highlight-green.png")
high_light_green = pygame.transform.scale(high_light_green, (checkers_red_img.get_rect().width + 7, checkers_red_img.get_rect().height + 7))
high_light = []
high_light_green_list = []
checkers_black = []
checkers_red = []
current_checker = []
high_light_white_list = []
high_light_red_list = []


class High_light_white(pygame.Rect):
    pass


class High_light_yellow(pygame.Rect):
    pass


class Checker_black(pygame.Rect):
    def __init__(self, *args):
        self.possible = []
        super().__init__(*args)

    def analysis(self):
        self.possible = []
        rx = self.x + self.width + self.width / 2
        ry = self.y + self.height + self.height / 2
        flag = True
        r_rect = pygame.Rect(rx, ry, 1, 1)
        for i in checkers_red:
            if r_rect.colliderect(i):
                flag = False
        for i in checkers_black:
            if r_rect.colliderect(i):
                flag = False
        if rx + 20 > min_size + (width - min_size) / 2:
            flag = False
        if flag:
            self.possible.append((self.x + self.width, self.y + self.height))
        rx = self.x - self.width / 2
        ry = self.y + self.height + self.height / 2
        flag2 = True
        r_rect = pygame.Rect(rx, ry, 1, 1)
        for i in checkers_red:
            if i.colliderect(r_rect):
                flag2 = False
        for i in checkers_black:
            if i.colliderect(r_rect):
                flag2 = False
        if rx < (width - min_size) / 2:
            flag2 = False
        if flag2:
            self.possible.append((self.x - self.width, self.y + self.height))
        return flag or flag2

    def move_to(self):
        r = random.choice(self.possible)
        for i in range(70):
            if self.x < r[0]:
                self.x += 1
            else:
                self.x -= 1
            self.y += 1
            update()


class Checker_red(pygame.Rect):
    def analysis(self):
        global high_light_red_list
        high_light_red_list = []
        global current_checker
        current_checker = [self]
        global high_light_green_list
        high_light_green_list = []
        rx = self.x - self.width
        flag = True
        ry = self.y - self.height
        r_rect = pygame.Rect(rx + self.width / 2, ry + self.height / 2, 1, 1)
        for i in checkers_red:
            if i.colliderect(r_rect):
                flag = False
        for i in checkers_black:
            if i.colliderect(r_rect):
                rect = pygame.Rect(rx - self.width, ry - self.height, 1, 1)
                collide = True
                for g in checkers_black:
                    if rect.colliderect(g):
                        collide = False
                for g in checkers_red:
                    if rect.colliderect(g):
                        collide = False
                if collide and (width - min_size) / 2 < rect.x < min_size + ((width - min_size) / 2) and rect.y - self.width > 0:
                    high_light_red_list.append(pygame.Rect(rect.x - 8, rect.y - 9, self.width, self.height))
                flag = False
        if rx < (width - min_size) / 2:
            flag = False
        if ry < 0:
            flag = False
        if flag:
            r_rect = pygame.Rect(rx - 5, ry - 8, high_light_green.get_rect().width, high_light_green.get_rect().height)
            if r_rect not in high_light_green_list:
                high_light_green_list.append(r_rect)
        rx = self.x + self.width
        ry = self.y - self.height
        flag = True
        r_rect = pygame.Rect(rx + 20, ry, 1, 1)
        for i in checkers_red:
            if i.colliderect(r_rect):
                flag = False
        for i in checkers_black:
            if i.colliderect(r_rect):
                rect = pygame.Rect(r_rect.x + self.width, r_rect.y - self.height, 1, 1)
                collide = True
                for g in checkers_black:
                    if rect.colliderect(g):
                        collide = False
                for g in checkers_red:
                    if rect.colliderect(g):
                        collide = False
                if collide and (width - min_size) / 2 < rect.x < min_size + ((width - min_size) / 2) and rect.y - self.height > 0:
                    high_light_red_list.append(pygame.Rect(rect.x - 20, rect.y - 9, self.width, self.height))
                flag = False
        if ry < 0:
            flag = False
        if rx + 20 > min_size + (width - min_size) / 2:
            flag = False
        if flag:
            r_rect = pygame.Rect(rx - 5, ry - 8, high_light_green.get_rect().width, high_light_green.get_rect().height)
            if r_rect not in high_light_green_list:
                high_light_green_list.append(r_rect)

    def move_to(self, x, y):
        right = True
        if self.x - x > 0:
            right = False
        for i in range((self.y - y - 5) // 2):
            if right:
                self.x += 2
            else:
                self.x -= 2
            self.y -= 2
            self.move(self.x, self.y)
            for i in checkers_black:
                if self.colliderect(i):
                    checkers_black.remove(i)
            update()
        global high_light_green_list
        global high_light
        high_light = []
        high_light_green_list = []


def move_enemy():
    possible_move = []
    for i in checkers_black:
        if i.analysis():
            possible_move.append(i)
    enemy = random.choice(possible_move)
    enemy.move_to()


def update():
    screen.fill((54, 109, 37))
    screen.blit(field_img, field_rect)
    for i in checkers_black:
        screen.blit(checkers_black_img, i)
    for i in checkers_red:
        screen.blit(checkers_red_img, i)
    for i in high_light:
        screen.blit(high_light_yellow, i)
    for i in high_light_green_list:
        screen.blit(high_light_green, i)
    for i in high_light_red_list:
        screen.blit(high_light_red, i)
    pygame.display.update()


for i in range(8):
    for g in range(3):
        if (i + g) % 2 == 1:
            continue
        checkers_red_rect = checkers_red_img.get_rect()
        checkers_red_rect.x = i * (min_size / 8 - 3) + (width - min_size) / 2 + 14
        checkers_red_rect.y = g * (min_size / 8 - 2) + 375
        checker_red = Checker_red(checkers_red_rect.x, checkers_red_rect.y, checkers_red_rect.width, checkers_red_rect.height)
        checkers_red.append(checker_red)
checkers_red_rect = checkers_red_img.get_rect()
checkers_red_rect.x = 615
checkers_red_rect.y = 515
field_rect.width = min_size
field_rect.height = min_size
screen = pygame.display.set_mode((width, height))
if height <= width:
    w = (width - height) / 2
    field_rect.x = w
else:
    w = (height - width) / 2
    field = pygame.Rect(0, w, min_size, min_size)
for i in range(8):
    for g in range(3):
        if (i + g) % 2 == 0:
            continue
        checkers_black_rect = checkers_black_img.get_rect()
        checkers_black_rect.x = i * (min_size // 8 - 3) + (width - min_size) / 2 + 14
        checkers_black_rect.y = g * (min_size / 8 - 2) + 10
        checker_black = Checker_black(checkers_black_rect.x, checkers_black_rect.y, checkers_black_rect.width, checkers_black_rect.height)
        checkers_black.append(checker_black)
fields = []
for i in range(8):
    for g in range(8):
        fields.append(pygame.Rect(i * min_size / 8, g * min_size / 8, min_size / 8, min_size / 8))
while True:
    events = pygame.event.get()
    for i in events:
        if i.type == pygame.MOUSEBUTTONDOWN:
            x, y = i.pos
            flag = True
            p = pygame.Rect(x, y, 1, 1)
            for g in high_light_red_list:
                if p.colliderect(g):
                    current_checker[0].move_to(g.x, g.y)
                    flag = False
            for e in checkers_red:
                if e.colliderect(p):
                    high = High_light_yellow(e.x - 3, e.y - 4, high_light_yellow.get_rect().width, high_light_yellow.get_rect().height)
                    if high_light:
                        high_light = [high]
                    else:
                        high_light.append(high)
                    e.analysis()
                    flag = False
            for green in high_light_green_list:
                if p.colliderect(green):
                    flag = False
                    current_checker[0].move_to(green.x, green.y)
                    move_enemy()
            if flag and p.colliderect(field_rect):
                high_light = []
                high_light_red_list = []
                high_light_green_list = []
        if i.type == pygame.QUIT:
            sys.exit()
    update()