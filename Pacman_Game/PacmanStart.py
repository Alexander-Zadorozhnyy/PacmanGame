"""
	Стартовое окно Pacman:
"""

import os
import sys
import pygame


with open('info_save.txt', 'w') as f:
    f.write(f'{str(0)}')
pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


BLACK = (0, 0, 0)

size = (1280, 720)

# Настройка экрана
screen = pygame.display.set_mode(size)

# Задатие названия
pygame.display.set_caption("Pacman")

# Загрузка картинки
Pacman = load_image('Pacman.png')

running = 1
screen.fill((BLACK))
i = 1

# Аудио файл
file = 'PacmanAudio.wav'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play()
# Первый затуск экрана

while running and i < 900:
    screen.fill((BLACK))
    screen.blit(Pacman, (i + 2, 400))
    pygame.display.flip()
    i += 1
pygame.display.quit()

##################################################################################################################
""" Проверка на нажатие кнопки старта"""


def main(button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position
            # Проверка мыши на кнопке
            if button.collidepoint(mouse_pos):
                return 0


##################################################################################################################
"""Второй экран"""

size = (1280, 720)

screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pacman")
screen.fill((BLACK))

# Загрузка всех изображений
Logo = load_image('Logo.png')
Logo = pygame.transform.scale(Logo, (640, 480))
Pacman = load_image('Pacman.png')
Pinky = load_image('Pinky.png')
Inky = load_image('Inky.png')
Blinky = load_image('Blinky.png')
Clyde = load_image('Clyde.png')
Ghost = load_image('Ghost1.png')
Play = load_image('PlayG.png')

running = 1
i = 1
button = pygame.Rect(600, 605, 95, 80)
pygame.draw.rect(screen, [0, 0, 0], button)  # рисование кнопки
while running:
    if main(button) == 0:
        # Если кнопка нажата:
        screen.fill(BLACK)
        break
    elif i < 500:
        screen.fill(BLACK)  # Заливка экрана

        screen.blit(Logo, (380, 100))
        # print(i,"Logo")

        screen.blit(Ghost, (i, 400))
        # print(i,"Ghost")

        screen.blit(Pacman, (i + 60, 400))
        # print(i+60,"Pacman")

        screen.blit(Pinky, (i + 120, 400))
        # print(i+120,"Pinky")

        screen.blit(Inky, (i + 180, 400))
        # print(i+180,"Inky")

        screen.blit(Blinky, (i + 240, 400))
        # print(i+240,"Blinky")

        screen.blit(Clyde, (i + 300, 400))
        # print(i+300,"Clyde")

        button = pygame.Rect(600, 605, 95, 80)

        pygame.draw.rect(screen, [0, 0, 0], button)  # draw button
        screen.blit(Play, (600, 600))
        pygame.display.flip()
        if main(button) == 0:
            break
    i += 1
    if main(button) == 0:
        break
os.system('python PacmanMain.py')
