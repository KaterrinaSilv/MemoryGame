import random
import sys

import pygame
from pygame.locals import *

from button import Button

pygame.init()

FPS = 30  # fps - общая скорость работы программы
WINDOWWIDTH = 640  # ширина окна в пикселях
WINDOWHEIGHT = 480  # высота
REVEALSPEED = 8  # скорость открытия ячеек
BOXSIZE = 40  # размер ячейки
GAPSIZE = 10  # расстояние медлу ячейками

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("res/background.jpg")

# цветовая палитра
#            R    G    B
LEMON = (255, 255, 153)
BEIGE = (153, 153, 255)
WHITE = (255, 255, 255)
BLUE = (153, 255, 204)
SIENA = (103, 54, 42)

BGCOLOR = BEIGE
LIGHTBGCOLOR = LEMON
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE


def get_font(size):
    return pygame.font.Font("res/a SignboardCpsNr BoldItalic.ttf", size)


# ЗНАЧЕНИЯ ЯЧЕЕК
CAT = 'cat'
CHAMELEON = 'chameleon'
CHICKEN = 'chicken'
COBRA = 'cobra'
DEER = 'deer'
DOG = 'dog'
DUCK = 'duck'
ELEPHANT = 'elephant'
OWL = 'owl'
PANDA = 'panda'

ALLSHAPES = (CAT, CHAMELEON, CHICKEN, COBRA, DEER, DOG, DUCK, ELEPHANT, OWL, PANDA)


def play(level_num):
    if (level_num == 1):
        BOARDWIDTH = 3  # количество колонок
        BOARDHEIGHT = 2  # количество строк
    elif (level_num == 2):
        BOARDWIDTH = 4
        BOARDHEIGHT = 3
    else:
        BOARDWIDTH = 5
        BOARDHEIGHT = 4

    assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'There must be an even number of blocks on the board'
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)  # рамка
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

    assert len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

    pygame.time.wait(250)
    pygame.init()
    pygame.font.init()

    font = pygame.font.Font(None, 36)

    LEVEL_TEXT = get_font(42).render(f'LEVEL:{level_num}', True, WHITE)
    LEVEL_RECT = LEVEL_TEXT.get_rect(
        center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 - WINDOWHEIGHT // 9))

    score = 0
    score_increment = 10
    score_decrease = -2

    mouseX = 0  # координаты курсора по ОХ
    mouseY = 0  # кооринаты курсора по ОУ
    pygame.display.set_caption('Play')

    mainBoard = getRandomizedBoard(BOARDWIDTH, BOARDHEIGHT)  # Создаем основное окно
    revealedBoxes = generateRevealedBoxesData(False, BOARDWIDTH, BOARDHEIGHT)  # Переворачиваем все карточки

    firstSelection = None  # Значения х у клика

    Display.display.fill(BGCOLOR)
    startGameAnimation(mainBoard, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)

    while True:  # main game loop
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        Display.display.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)

        Display.display.blit(LEVEL_TEXT, LEVEL_RECT)

        PLAY_BACK = Button(image=pygame.image.load("res/button_menu.png"),
                           pos=(WINDOWWIDTH - WINDOWWIDTH // 10, WINDOWHEIGHT // 14))
        PLAY_BACK.update(SCREEN)

        mouseClicked = False
        score_text = font.render(f'Score: {score}', True, BLUE)

        for event in pygame.event.get():  # event handling loop
            Display.display.blit(score_text, (10, 10))
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mouseX, mouseY, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)
        if boxx != None and boxy != None:
            # В момент, когда курсор находится на ячейке
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy, XMARGIN, YMARGIN)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)], XMARGIN, YMARGIN)
                revealedBoxes[boxx][boxy] = True  # "открываем карточку"
                if firstSelection == None:  # карточка была открыта первой
                    firstSelection = (boxx, boxy)
                else:
                    # Проверим есть ли совпадение между иконками
                    icon1 = getIconValue(mainBoard, firstSelection[0], firstSelection[1])
                    icon2 = getIconValue(mainBoard, boxx, boxy)

                    if icon1 != icon2:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)], XMARGIN,
                                            YMARGIN)
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                        score += score_decrease
                    elif hasWon(revealedBoxes):  # все ли карточки открыты?
                        score += score_increment
                        gameWonAnimation(mainBoard, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)
                        pygame.time.wait(2000)
                        if (level_num != 3):
                            next_level(score, level_num + 1)
                        else:
                            congratulation_screen()
                        score = 0
                    else:
                        score += score_increment

                    firstSelection = None  # обновляем х у клик

        Display.display.blit(score_text, (10, 10))

        # Отрисовка экрана
        pygame.display.update()
        FpsClock.fpsClock.tick(FPS)


def levels():
    while True:
        pygame.time.wait(250)
        SCREEN.blit(BG, (0, 0))

        LEVEL_MENU_TEXT = get_font(42).render("CHOOSE A LEVEL:", True, WHITE)
        LEVEL_MENU_RECT = LEVEL_MENU_TEXT.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 - WINDOWHEIGHT // 9))

        LEVEL_MENU_MOUSE_POS = pygame.mouse.get_pos()

        LEVEL1 = Button(image=pygame.image.load("res/button_level.png"),
                        pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - WINDOWHEIGHT // 8))
        LEVEL2 = Button(image=pygame.image.load("res/button_level2.png"),
                        pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + WINDOWHEIGHT // 4 - WINDOWHEIGHT // 8))
        LEVEL3 = Button(image=pygame.image.load("res/button_level3.png"),
                        pos=(WINDOWWIDTH // 2, WINDOWHEIGHT - WINDOWHEIGHT // 8))

        SCREEN.blit(LEVEL_MENU_TEXT, LEVEL_MENU_RECT)

        for button in [LEVEL1, LEVEL2, LEVEL3]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL1.checkForInput(LEVEL_MENU_MOUSE_POS):
                    play(1)
                if LEVEL2.checkForInput(LEVEL_MENU_MOUSE_POS):
                    play(2)
                if LEVEL3.checkForInput(LEVEL_MENU_MOUSE_POS):
                    play(3)

        pygame.display.update()


def next_level(score, level_num):
    while True:
        pygame.time.wait(250)
        SCREEN.blit(BG, (0, 0))

        CONTINUE_MENU_TEXT = get_font(40).render(f'Congratulations! YOUR SCORE:{score}', True, WHITE)
        CONTINUE_MENU_RECT = CONTINUE_MENU_TEXT.get_rect(
            center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 - WINDOWHEIGHT // 9))

        CONTINUE_MENU_MOUSE_POS = pygame.mouse.get_pos()

        CONTINUE = Button(image=pygame.image.load("res/button_sontinue.png"),
                          pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - WINDOWHEIGHT // 8))

        SCREEN.blit(CONTINUE_MENU_TEXT, CONTINUE_MENU_RECT)

        CONTINUE.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CONTINUE.checkForInput(CONTINUE_MENU_MOUSE_POS):
                    play(level_num)

        pygame.display.update()


def congratulation_screen():
    while True:
        pygame.time.wait(250)
        SCREEN.blit(BG, (0, 0))

        CONGRAT_TEXT = get_font(24).render("Congratulations, you have passed the game!", True, SIENA)
        CONGRAT_RECT = CONGRAT_TEXT.get_rect(
            center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 - WINDOWHEIGHT // 9))

        A_TEXT = get_font(24).render("Author: Serebriakova Ekaterina", True, SIENA)
        A_RECT = CONGRAT_TEXT.get_rect(
            center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4))

        CONGRAT_MOUSE_POS = pygame.mouse.get_pos()

        MENU = Button(image=pygame.image.load("res/button_menu.png"),
                      pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))

        SCREEN.blit(CONGRAT_TEXT, CONGRAT_RECT)
        SCREEN.blit(A_TEXT, A_RECT)

        MENU.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU.checkForInput(CONGRAT_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(42).render("WELCOME TO MEMORY GAME!", True, WHITE)
        MENU_RECT = MENU_TEXT.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 4 - WINDOWHEIGHT // 9))

        PLAY_BUTTON = Button(image=pygame.image.load("res/button_play.png"),
                             pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 - WINDOWHEIGHT // 8))
        OPTIONS_BUTTON = Button(image=pygame.image.load("res/button_levels.png"),
                                pos=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + WINDOWHEIGHT // 4 - WINDOWHEIGHT // 8))
        QUIT_BUTTON = Button(image=pygame.image.load("res/button_quit.png"),
                             pos=(WINDOWWIDTH // 2, WINDOWHEIGHT - WINDOWHEIGHT // 8))

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(1)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    levels()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def generateRevealedBoxesData(val, BOARDWIDTH, BOARDHEIGHT):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


def getRandomizedBoard(BOARDWIDTH, BOARDHEIGHT):
    # Получаем список всех возможных цветов и иконок
    icons = []
    for icon in ALLSHAPES:
        icons.append(icon)

    random.shuffle(icons)  # Рандомизируем порядок иконок
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # Вычисляем количество иконок
    icons = icons[:numIconsUsed] * 2  # Создаем пары
    random.shuffle(icons)

    # Создадим список, где рандомно расположим иконки
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy, XMARGIN, YMARGIN):
    # Преобразуем координаты доски в пиксельные координаты
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy, XMARGIN, YMARGIN)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def drawIcon(icon, boxx, boxy, XMARGIN, YMARGIN):
    left, top = leftTopCoordsOfBox(boxx, boxy, XMARGIN, YMARGIN)  # получим пиксельные координаты из координат доски
    # Draw the shapes
    if icon == OWL:
        image_serf = pygame.image.load('res/images/free-icon-owl-10875949.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == CAT:
        image_serf = pygame.image.load('res/images/free-icon-cat-10875910.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == CHAMELEON:
        image_serf = pygame.image.load('res/images/free-icon-chameleon-10875911.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == CHICKEN:
        image_serf = pygame.image.load('res/images/free-icon-chicken-10875912.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == COBRA:
        image_serf = pygame.image.load('res/images/free-icon-cobra-10875913.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == DEER:
        image_serf = pygame.image.load('res/images/free-icon-deer-10875916.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == DOG:
        image_serf = pygame.image.load('res/images/free-icon-dog-10875917.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == DUCK:
        image_serf = pygame.image.load('res/images/free-icon-duck-10875918.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == ELEPHANT:
        image_serf = pygame.image.load('res/images/free-icon-elephant-10875922.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))
    elif icon == PANDA:
        image_serf = pygame.image.load('res/images/free-icon-panda-10875951.png')
        image_serf = pygame.transform.scale(image_serf, (BOXSIZE, BOXSIZE))
        Display.display.blit(image_serf, (left, top))


def getIconValue(board, boxx, boxy):
    # значения иконок x, y сохраняются в board[x][y][0]
    return board[boxx][boxy]


def drawBoxCovers(board, boxes, coverage, XMARGIN, YMARGIN):
    # Отрисовываем ячейки
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1], XMARGIN, YMARGIN)
        pygame.draw.rect(Display.display, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        icon = getIconValue(board, box[0], box[1])
        drawIcon(icon, box[0], box[1], XMARGIN, YMARGIN)
        if coverage > 0:
            pygame.draw.rect(Display.display, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FpsClock.fpsClock.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal, XMARGIN, YMARGIN):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage, XMARGIN, YMARGIN)


def coverBoxesAnimation(board, boxesToCover, XMARGIN, YMARGIN):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage, XMARGIN, YMARGIN)


def drawBoard(board, revealed, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy, XMARGIN, YMARGIN)
            if not revealed[boxx][boxy]:
                # Рисуем перевернутую ячейку
                pygame.draw.rect(Display.display, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Рисуем иконку
                icon = getIconValue(board, boxx, boxy)
                drawIcon(icon, boxx, boxy, XMARGIN, YMARGIN)


def drawHighlightBox(boxx, boxy, XMARGIN, YMARGIN):
    left, top = leftTopCoordsOfBox(boxx, boxy, XMARGIN, YMARGIN)
    pygame.draw.rect(Display.display, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN):
    # Переворачиваем 8 рандомных карточек
    coveredBoxes = generateRevealedBoxesData(False, BOARDWIDTH, BOARDHEIGHT)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup, XMARGIN, YMARGIN)
        coverBoxesAnimation(board, boxGroup, XMARGIN, YMARGIN)


def gameWonAnimation(board, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN):
    coveredBoxes = generateRevealedBoxesData(True, BOARDWIDTH, BOARDHEIGHT)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        Display.display.fill(color1)
        drawBoard(board, coveredBoxes, BOARDWIDTH, BOARDHEIGHT, XMARGIN, YMARGIN)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


class FpsClock:
    fpsClock = pygame.time.Clock()


class Display:
    display = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))


main_menu()
