"""
	Запуск главного экрана:
"""

# Загрузка импортов
import pygame
import random
from pynput import keyboard
import numpy
from numpy import loadtxt
import time
import sys
import os
import datetime

# Настройка времени
clock = pygame.time.Clock()
with open('info_save.txt', 'r') as f:
    file = f.readline()
with open('colors_for_level_wall.txt', 'r') as f:
    colors = list(map(lambda x: x.split('$'), list(map(lambda x: str(x)[:-1], f.readlines()))))
levels = ['Levels\level1.1.txt', 'Levels\level2.1.txt']

# Обозначение констант
WIDTH, HEIGHT = (22, 22)
WALL_COLOR = pygame.Color(eval(colors[int(file)][0]))
GREY = pygame.Color('grey')  # GREY
PACMAN_COLOR = pygame.Color(0, 255, 0)
GHOST_COLOR = pygame.Color(255, 0, 0)
COIN_COLOR = pygame.Color(255, 255, 0)  # YELLOW
PORTAL_COLOR = pygame.Color(0, 255, 255)
TEXT_COLOR = pygame.Color(0, 0, 0)  # BLACK
GAME_TOPLEFT = (0, HEIGHT)
GAME_BCKGRND = (0, 0, 100)  # BLACK
MENU_BCKGRND = (0, 128, 128)  # BLUE_GREEN
MENU_BORDER = pygame.Color(128, 128, 0)  # BROWN

DOWN = (0, 1)
RIGHT = (1, 0)
UP = (0, -1)
LEFT = (-1, 0)
NONE = (0, 0)


# Функция обработки изображения
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


# Обозначение функций рисования для каждого из возможных объеетов.
# Функция рисования блока - стена
def draw_wall(screen, pos):
    pixels = pixels_from_points(pos)
    pixels = (pixels[0] + GAME_TOPLEFT[0], pixels[1] + GAME_TOPLEFT[1])
    pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])


# тип создаваемого enemy для дальнейшей функции
count_enemy_stules = 0


# Функция проверки на тип объекта + его создание
def trytoplotimage(pixels, type_of_enemy):
    change = tuple(pixels)
    # Если объест PacMan
    if type_of_enemy == 'Pacman':
        # print(change)
        # print(change[0])
        change = (change[0] - 5, change[1] - 5)
        PacMan = load_image('PacmanEat.png')
        PacMan = pygame.transform.scale(PacMan, (WIDTH + 5, HEIGHT + 5))
        screen.blit(PacMan, [change, (WIDTH, HEIGHT)])
    # Если объест Ghost
    elif type_of_enemy == 'Ghost':
        # print(change)
        # print(change[0])
        # Pacman = pygame.image.load('pac-man.png')
        # PacMan = pygame.transform.scale(screen,(WIDTH, HEIGHT))
        # screen.blit(Pacman,[change, (WIDTH, HEIGHT)])
        # time.sleep(1)
        # Добавить различных монстров
        ghost = None
        # Проверка на то, какой buster активирован
        if count_enemy_stules == 0:
            ghost = load_image('Pinky1.png')
        elif count_enemy_stules == 2:
            ghost = load_image('Clyde1.png')
        elif count_enemy_stules == 1:
            ghost = load_image('Ghost12.png')
        elif count_enemy_stules == 4:
            ghost = load_image('Inky1.png')

        ghost = pygame.transform.scale(ghost, (WIDTH + 5, HEIGHT + 5))
        screen.blit(ghost, [change, (WIDTH, HEIGHT)])
    # Если объест Cherry - невидимость
    elif type_of_enemy == 'cherry':
        cherry = load_image('cherry.png')
        cherry = pygame.transform.scale(cherry, (WIDTH, HEIGHT))
        screen.blit(cherry, [change, (WIDTH, HEIGHT)])
    # Если объест Strawberry - замедление
    elif type_of_enemy == 'strawberry':
        strawbery = load_image('strawberry.png')
        strawbery = pygame.transform.scale(strawbery, (WIDTH, HEIGHT))
        screen.blit(strawbery, [change, (WIDTH, HEIGHT)])


# Рисование персонажа
def draw_pacman(pos):
    pixels = pixels_from_points(pos)
    pixels = (pixels[0] + GAME_TOPLEFT[0], pixels[1] + GAME_TOPLEFT[1])
    trytoplotimage(pixels, 'Pacman')


# рисование enemy
def draw_ghost(pos):
    pixels = pixels_from_points(pos)
    pixels = (pixels[0] + GAME_TOPLEFT[0], pixels[1] + GAME_TOPLEFT[1])
    trytoplotimage(pixels, 'Ghost')


# Отрисовка монет
def draw_coin(screen, pos):
    pixels = pixels_from_points(pos)
    pixels = (pixels[0] + 10, pixels[1] + GAME_TOPLEFT[1] + 10)
    pygame.draw.ellipse(screen, COIN_COLOR, (pixels, (WIDTH / 4, HEIGHT / 4)))


# Отрисовка busters
def draw_powerup(screen, pos, type_power):
    pixels = pixels_from_points(pos)
    pixels = (pixels[0] + GAME_TOPLEFT[0], pixels[1] + GAME_TOPLEFT[1])
    pos = (pos[0] + GAME_TOPLEFT[0] // WIDTH, pos[1] + GAME_TOPLEFT[1] // HEIGHT)
    if type_power == 'blink':
        pygame.draw.circle(screen, GREY, (pos[0] * WIDTH + WIDTH // 2, pos[1] * HEIGHT + HEIGHT // 2), WIDTH // 4)
    if type_power == 'cherry':
        trytoplotimage(pixels, 'cherry')
    if type_power == 'strawberry':
        trytoplotimage(pixels, 'strawberry')


# Отрисовка меню со всеми показателями игры
def draw_menu(screen, life_left, points, time_taken):
    timeDone = time.time() - time_start
    screen.blit(text.render('Осталось жизней: ' + str(life_left), True, TEXT_COLOR), (0, HEIGHT // 3))
    screen.blit(text.render('Очки: ' + str(points), True, TEXT_COLOR), (cols * WIDTH // 3, HEIGHT // 3))
    screen.blit(text.render('Время: ' + str(time_taken), True, TEXT_COLOR), (2 * cols * WIDTH // 3, HEIGHT // 3))


# Отрисовка порталов для перемещения в соответствии со своим номером.
def draw_portal(screen, pos, number):
    pos = (pos[0] + GAME_TOPLEFT[0] // WIDTH, pos[1] + GAME_TOPLEFT[1] // HEIGHT)
    plist = [(pos[0] * WIDTH, pos[1] * HEIGHT + HEIGHT),
             (pos[0] * WIDTH + WIDTH // 4, pos[1] * HEIGHT + HEIGHT // 4),
             (pos[0] * WIDTH + 3 * WIDTH // 4, pos[1] * HEIGHT + HEIGHT // 4),
             (pos[0] * WIDTH + WIDTH, pos[1] * HEIGHT + HEIGHT),
             (pos[0] * WIDTH, pos[1] * HEIGHT + HEIGHT)
             ]
    pygame.draw.polygon(screen, PORTAL_COLOR, plist)
    screen.blit(text.render(number, True, TEXT_COLOR), (pos[0] * WIDTH + WIDTH // 3, pos[1] * HEIGHT + HEIGHT // 4))


# Инициализация самого пакмана Класс.
class PacMan:
    move_direction = DOWN

    def __init__(self):
        self.x = int(colors[int(file)][1][-1])
        self.y = int(colors[int(file)][1][0])

    def position(self):
        return self.x, self.y

    def display(self):
        draw_pacman((self.x, self.y))

    def moveTo(self, x, y):
        self.x = x
        self.y = y


# Инициализация busterов. Их обозначения на карте
SPEED_PU_COLOR = pygame.Color(235, 34, 228, 255)
GHOSTHUNTER_PU_COLOR = pygame.Color(235, 215, 34, 255)
INVISIBLE_PU_COLOR = pygame.Color(115, 125, 116, 255)

POWER_NONE = ('', PACMAN_COLOR)
POWER_SPEEDUP = ('s', SPEED_PU_COLOR)
POWER_GHOSTHUNTER = ('k', GHOSTHUNTER_PU_COLOR)
POWER_INVISIBLE = ('i', INVISIBLE_PU_COLOR)


# Функции для получения позиций в определенном направлении.
def add_to_pos(pos, pos2):
    return pos[0] + pos2[0], pos[1] + pos2[1]


# Фунция перевода коордитатных позиций в пиксельные размеры
def pixels_from_points(pos):
    return pos[0] * WIDTH, pos[1] * HEIGHT


# Инициализация pygame и переменных для уровня
layout = loadtxt(levels[int(file)], dtype=str)
rows, cols = layout.shape
pygame.display.init()
pygame.font.init()
basic_f = pygame.font.get_default_font()
text = pygame.font.Font(basic_f, 5 * HEIGHT // 8)

screen = pygame.display.set_mode((cols * WIDTH + GAME_TOPLEFT[0], rows * HEIGHT + GAME_TOPLEFT[1]), 0, 32)
game_background = pygame.surface.Surface((cols * WIDTH, rows * HEIGHT)).convert()
menu_background = pygame.surface.Surface((cols * WIDTH, GAME_TOPLEFT[1])).convert()
time.sleep(2)


# Класс, в котором реализованы порталы.
class Portals:
    portal_links = {}
    jump_loc = (-1, -1)

    def add(self, x, y, num):
        try:
            src = Portals.portal_links[num]
            Portals.portal_links[src] = (x, y)
            Portals.portal_links.pop(num)
            Portals.portal_links.update([[(x, y), src]])
        except KeyError:
            Portals.portal_links.update([[num, (x, y)], [(x, y), num]])

    def check(self, x, y):
        if Portals.jump_loc != (x, y):
            Portals.jump_loc = (-1, -1)
            return Portals.portal_links.get((x, y))
        return None

    def exec_jump(self, x, y):
        global pacman
        pacman.x, pacman.y = Portals.portal_links[(x, y)]
        Portals.jump_loc = (pacman.x, pacman.y)


# Получение и обработка и добавление позиций enemy в общий список.
ghost_positions = []
portal = Portals()
for y in range(len(layout)):
    ghost_positions.extend([(x, y) for x, val in enumerate(layout[y]) if val == 'O'])
    for x in range(len(layout[y])):
        if layout[y][x] >= '1' and layout[y][x] < '9':
            portal.add(x, y, layout[y][x])

game_background.fill(GAME_BCKGRND)
menu_background.fill(MENU_BCKGRND)


# Функция, обрабатывающая нажатие на клавишу и изменяющая направление передвижения главного героя.
def set_direction(key):
    try:
        print(f'нажата  {key.char} клавиша')
        if key.char == 'w':
            PacMan.move_direction = UP
        if key.char == 'a':
            PacMan.move_direction = LEFT
        if key.char == 's':
            PacMan.move_direction = DOWN
        if key.char == 'd':
            PacMan.move_direction = RIGHT
    except AttributeError:
        pass
    return looping


# Функция генерации рандомной позиции для передвижения призраков.
def random_pos(pos):
    global direction
    rand = [UP, DOWN, RIGHT, LEFT]
    direction = rand[random.randint(0, 3)]
    try:
        if pos[1] + direction[1] >= 36 or pos[0] + direction[0] >= 28 or pos[1] + direction[1] <= 0 or pos[0] + \
                direction[0] <= 0:
            print(pos, pos[1] + direction[1], pos[0] + direction[0])
            pos = (18, 14)
        elif layout[pos[1] + direction[1]][pos[0] + direction[0]] == 'w':
            direction = NONE
            random_pos(pos)
            # print("This is randomly generated: ", direction)
    except IndexError:
        print(pos)
        pos = (18, 14)
    return add_to_pos(pos, direction)


# Переменные направлений
last_pos = ()

# Функция погони призраков за пакманом
def chase(x, y, pos):
    global last_pos
    '''
    Avoided This and switched to Randomness as it would make movements unpredictable
    '''
    if x < pos[0] and layout[pos[1]][pos[0] - 1] != 'w':
        pos = add_to_pos(pos, LEFT)
    if x > pos[0] and layout[pos[1]][pos[0] + 1] != 'w':
        pos = add_to_pos(pos, RIGHT)
    if y < pos[1] and layout[pos[1] - 1][pos[0]] != 'w':
        pos = add_to_pos(pos, UP)
    if y > pos[1] and layout[pos[1] + 1][pos[0]] != 'w':
        pos = add_to_pos(pos, DOWN)
    last_pos = (x, y)
    return pos


# Функция побега от пакмана во время действия buster
def flee(x, y, pos):
    '''
    Avoided This and switched to Randomness as it would make movements unpredictable,
    enabling the pacman to earn more points.
    '''
    if x < pos[0] and layout[pos[1]][pos[0] + 1] != 'w':
        pos = add_to_pos(pos, RIGHT)
    elif x > pos[0] and layout[pos[1]][pos[0] - 1] != 'w':
        pos = add_to_pos(pos, LEFT)
    elif y < pos[1] and layout[pos[1] + 1][pos[0]] != 'w':
        pos = add_to_pos(pos, DOWN)
    elif y > pos[1] and layout[pos[1] - 1][pos[0]] != 'w':
        pos = add_to_pos(pos, UP)
    return pos


pacman = PacMan()


# Класс отвечающий за busterы
class PowerUP:
    power = POWER_NONE
    timer = 0
    flag = 0

    def __init__(self):
        self.points = 0

    # счетчик действия ускорителя
    def tic(self):
        global count_enemy_stules
        # If using a power-up,
        if PowerUP.power[0] != '':
            # If time has run out, remove power_up
            if PowerUP.timer == 0:
                PowerUP.power = POWER_NONE
                count_enemy_stules = 0
            # Else decrease the time left
            else:
                PowerUP.timer -= 1

    # Проверка на активацию ускорителя и проигровки соответствующего звука.
    def check(self, y, x):
        global count_enemy_stules
        # If come in contact with a power-up, grab it!
        if layout[y][x] == 's':
            PowerUP.power = POWER_SPEEDUP
            PowerUP.timer = 45
            layout[y][x] = '.'
            # Audio File
            file_au = 'pacman_chomp1.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file_au)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            count_enemy_stules = 4
        if layout[y][x] == 'i':
            PowerUP.power = POWER_INVISIBLE
            PowerUP.timer = 30
            layout[y][x] = '.'
            # Audio File
            file_au = 'pacman_chomp1.wav'
            pygame.mixer.init()
            pygame.mixer.music.load(file_au)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            count_enemy_stules = 1
        if layout[y][x] == 'k':
            PowerUP.power = POWER_GHOSTHUNTER
            PowerUP.timer = 60
            layout[y][x] = '.'
            # Audio File
            file_au = 'pacman_chomp1.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file_au)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            count_enemy_stules = 2
        # coin should dissapear when eating, i.e update the layout array
        if layout[y][x] == 'c':
            layout[y][x] = '.'
            # Audio File
            file_au = 'pacman_chomp.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file_au)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            self.points += 5
        if layout[y][x] == '.':
            # Audio File
            file_au = 'pacman_vague.wav'
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(file_au)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            self.points += 0

    def execute(self):
        global ghost_positions
        global lives
        # Если используется скорость 0.5x
        if PowerUP.power[0] == 's':
            # Если первый раз (flag=1), пропуск хода призрака, и flag=0
            if PowerUP.flag == 1:
                PowerUP.flag = 0
                # Время спать.
                return 1
            # Если изначально flag = 0, то наоборот и flag=1
            else:
                PowerUP.flag = 1

        # Если используется ускоритель - невидимость, ghost перемещается рандомно.
        if PowerUP.power[0] == 'i':
            ghost_positions = [random_pos(pos) for pos in ghost_positions]
        # Если используется ускоритель - ghosthunter, ghost будет убегать от вас.
        elif PowerUP.power[0] == 'k':
            ghost_positions = [random_pos(pos) for pos in ghost_positions]
        # Если ничего не активировано, ghost будет преследовать вас.
        else:
            ghost_positions = [random_pos(pos) for pos in ghost_positions]

        # Если произойдет столкновение с призраком:
        if any([pacman.position() == ghost_position for ghost_position in ghost_positions]):
            # Если включен ghosthunter вы убьете призрака
            if PowerUP.power[0] == 'k':
                for pos in ghost_positions[:]:
                    if pos == pacman.position():
                        ghost_positions.remove(pos)
                        ghost_positions.extend([(13, 18)])
            # Иначе, вы возродитесь на старте и потеряете жизнь.
            elif PowerUP.power[0] != 'i':
                pacman.x = int(colors[int(file)][1][-1])
                pacman.y = int(colors[int(file)][1][0])
                self.points -= 1
                lives -= 1
        return 0.15


power = PowerUP()
looping = True
time_start = time.time()
lives = 3
# Получение команд от клавиатуры.
kl = keyboard.Listener(on_press=set_direction, on_release=None)
kl.start()
writingfont = pygame.font.SysFont('comicsansms', 25)

# Основной игровой цикл.
while looping:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False
            lives = 0

    # Если игрок выиграл или проиграл игра заканчивается.
    if lives == 0 or not any(['c' in row for row in layout]):
        looping = False

    # Запуск меню проигрыша.
    screen.blit(menu_background, (0, 0))
    screen.blit(game_background, GAME_TOPLEFT)
    draw_menu(screen, lives, power.points, time.time() - time_start)

    # Рисуем поле игры из txt файла
    for col in range(cols):
        for row in range(rows):
            value = layout[row][col]
            pos = (col, row)
            if value == 'w':
                draw_wall(screen, pos)
            elif value == 'c':
                draw_coin(screen, pos)
            elif value == 's':
                draw_powerup(screen, pos, 'strawberry')
            elif value == 'i':
                draw_powerup(screen, pos, 'cherry')
            elif value == 'k':
                draw_powerup(screen, pos, 'blink')
            elif value >= '1' and value <= '9':
                draw_portal(screen, pos, value)

    # Рисуем игрока.
    pacman.display()

    # Рисуем призраков.
    for position in ghost_positions:
        draw_ghost(position)

    # Если заходим в один портал выходим из другого с таким же номером.
    if portal.check(pacman.x, pacman.y) != None:
        portal.exec_jump(pacman.x, pacman.y)
    # Если только что переместились пропускаем ход.

    # Получаем следующую координату для перемещения
    next_x = (pacman.x + PacMan.move_direction[0]) % cols
    next_y = (pacman.y + PacMan.move_direction[1]) % rows

    # Проверка на то, что находится в следующей клетке
    power.check(next_y, next_x)
    power.tic()

    # Обновление позиции игрока в соответствии с проверкой.
    # Перемещение если следующий блок не стена.
    if layout[next_y][next_x] != 'w':
        pacman.moveTo(next_x, next_y)

    # если бустер включен обрабатываем его.
    sleep = power.execute()

    # Обновление экрана
    pygame.display.update()

    # Ждем обновления.
    time.sleep(sleep)

# Проверка на выигрыш или проигрыш
if lives > 0:
    if int(file) + 1 == len(levels):
        times = time.time()
        size = (640, 480)
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pacman")
        writingfont = pygame.font.SysFont('comicsansms', 100)
        running = 1
        i = 1
        # Цикл экрана проигрыша
        while running:
            Pacman = load_image('Ghost.png')
            Pac = load_image('Youwin.jpg')
            while running and i < 2000:
                screen.fill(WALL_COLOR)
                screen.blit(Pac, (0, 0))
                screen.blit(Pacman, (numpy.random.randint(1280), numpy.random.randint(1280)))
                text = writingfont.render(f"Ваш счет: {str(power.points)}", True, TEXT_COLOR)
                text2 = writingfont.render(f"Пройдено уровней:{str(int(file) + 1)}", True, TEXT_COLOR)
                text3 = writingfont.render(f"Время в игре: {round(times - time_start, 2)} секунд.", True, TEXT_COLOR)
                screen.blit(text, [250, 355])
                screen.blit(text2, [250, 380])
                screen.blit(text3, [250, 405])
                pygame.display.flip()
            pygame.display.quit()
            with open('info_save.txt', 'w') as f:
                f.write(f'{str(0)}')
            with open('scoring.txt', 'a') as w:
                w.write(f'{str(power.points)} Win Level - {str(file)} /')
            kl.stop()
            break
    else:
        print("YOU WIN!")
        print("You won", power.points, "points!")
        with open('info_save.txt', 'w') as f:
            f.write(f'{str(int(file) + 1)}')
        with open('scoring.txt', 'a') as w:
            w.write(f'{str(power.points)} Win Level - {str(file)} /')
        os.system('python PacmanMain.py')
else:
    times = time.time()
    # Аудио файл
    file_au = 'sad.wav'
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_au)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
    today = datetime.datetime.today()
    print("You Lost!")
    # Сохранение результата игры
    with open('scoring.txt', 'a') as w:
        w.write(f'{str(power.points)} Lost - {today.strftime("%Y-%m-%d-%H.%M.%S")} \n')
    size = (580, 580)
    scoring = 0
    with open('money.txt', 'r') as score:
        print('dfdsdsff')
        scoring = int(score.readline())
        scoring = scoring + power.points
    with open('money.txt', 'w') as score:
        score.write(str(scoring))

    # Найстройка экрана.
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pacman")
    running = 1
    i = 1
    # Цикл экрана проигрыша
    while running:
        Pacman = load_image('Ghost.png')
        Pac = load_image('GameOver.jpg')
        while running and i < 2000:
            screen.fill(WALL_COLOR)
            screen.blit(Pac, (40, 10))
            font = pygame.font.Font(None, 25)
            text = font.render(f"Ваш счет: {str(power.points)}", True, TEXT_COLOR)
            text2 = font.render(f"Пройдено уровней:{str(int(file) + 1)}", True, TEXT_COLOR)
            text3 = font.render(f"Время в игре: {round(times - time_start, 2)} секунд.", True, TEXT_COLOR)
            screen.blit(text, [150, 400])
            screen.blit(text2, [150, 440])
            screen.blit(text3, [150, 480])
            screen.blit(Pacman, (numpy.random.randint(1280), numpy.random.randint(1280)))
            pygame.display.flip()
            i += 1
        pygame.display.quit()
        kl.stop()
        break
    time.sleep(10)
    sys.exit()
