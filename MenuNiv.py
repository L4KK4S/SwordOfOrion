import pygame
from pygame import mixer
import time

pygame.init()

clock = pygame.time.Clock()
FPS = 30

screen_width = 800
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SwordOfOrion - Niveaux')


#load images
bg_img = pygame.image.load('data/menuNivBackGround.jpg')
red_flag_temp = pygame.image.load('data/redFlag.png')
red_flag  = pygame.transform.scale(red_flag_temp, (120, 120))
big_red_flag  = pygame.transform.scale(red_flag_temp, (200, 200))
green_flag_temp = pygame.image.load('data/greenFlag.png')
green_flag  = pygame.transform.scale(green_flag_temp, (120, 120))
big_green_flag  = pygame.transform.scale(green_flag_temp, (200, 200))
ok_flag_temp = pygame.image.load('data/greenFlagOK.png')
ok_flag = pygame.transform.scale(ok_flag_temp, (120, 120))
ok_flag_big = pygame.transform.scale(ok_flag_temp, (200, 200))
triangle_temp = pygame.image.load('data/triangle2.png')
triangle = pygame.transform.scale(triangle_temp, (35, 35))

#load textes
myfont = pygame.font.Font("data/future.ttf", 30)
lvl1 = myfont.render("lvl1", 1, (255, 255, 255))
lvl2 = myfont.render("lvl2", 1, (255, 255, 255))
lvl3 = myfont.render("lvl3", 1, (255, 255, 255))
lvl4 = myfont.render("lvl4", 1, (255, 255, 255))
lvl5 = myfont.render("lvl5", 1, (255, 255, 255))

#load music
mixer.init()
mixer.music.load("data/MenuNiv.wav")
mixer.music.set_volume(0.9)
mixer.music.play(-1)
ok = pygame.mixer.Sound('data/okBtn.wav')
select = pygame.mixer.Sound('data/selectBtn.wav')

#load variables
tours = 0
image = True
endroit = 1
toucheR = True
toucheF = True
nv = 0

run = True
while run:

    tours += 1

    text = open("data/Sauvegarde.txt", "r")
    l = []
    for i in text:
        if i[2] == "O":
            l.append(True)
        else:
            l.append(False)
    text.close()

    text = open("data/Sauvegarde.txt", "r")
    l2 = []
    for i in text:
        if i[3] == "O":
            l2.append(True)
        else:
            l2.append(False)
    text.close()

    print(l2)

    screen.blit(bg_img, (0, 0))


    if l2[0] == True:
        screen.blit(ok_flag, (50, 50))
    elif l[0] == True:
        screen.blit(green_flag, (50, 50))
    else:
        screen.blit(green_flag, (50, 50))
    screen.blit(lvl1, (80, 140))

    if l2[1] == True:
        screen.blit(ok_flag, (200, 30))
    elif l[1] == True:
        screen.blit(green_flag, (200, 30))
    else:
        screen.blit(red_flag, (200, 30))
    screen.blit(lvl2, (230, 120))

    if l2[2] == True:
        screen.blit(ok_flag, (350, 80))
    elif l[2] == True:
        screen.blit(green_flag, (350, 80))
    else:
        screen.blit(red_flag, (350, 80))
    screen.blit(lvl3, (380, 170))

    if l2[3] == True:
        screen.blit(ok_flag, (500, 40))
    elif l[3] == True:
        screen.blit(green_flag, (500, 40))
    else:
        screen.blit(red_flag, (500, 40))
    screen.blit(lvl4, (530, 130))

    if l2[4] == True:
        screen.blit(ok_flag_big, (600, 40))
    elif l[4] == True:
        screen.blit(big_green_flag, (600, 40))
    else:
        screen.blit(big_red_flag, (600, 40))
    screen.blit(lvl5, (660, 185))

    if tours%10 == 0 and tours != 0:
        if image == True:
            image = False
        else:
            image = True

    if image == True:
        if endroit == 1:
            screen.blit(triangle, (90, 20))
        elif endroit == 2:
            screen.blit(triangle, (240, 5))
        elif endroit == 3:
            screen.blit(triangle, (390, 50))
        elif endroit == 4:
            screen.blit(triangle, (540, 10))
        elif endroit == 5:
            screen.blit(triangle, (680, 20))

    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT] and endroit != 5 and toucheR == True:
        toucheR = False
        if l[endroit] == True:
            select.play()
            endroit += 1
    if key[pygame.K_LEFT] and endroit != 1 and toucheF == True:
        select.play()
        toucheF = False
        endroit -= 1
    if key[pygame.K_RETURN]:
        ok.play()
        time.sleep(0.4)
        nv = endroit
        run = False

    if tours % 15 == 0 and toucheR == False:
        toucheR = True

    if tours % 15 == 0 and toucheF == False:
        toucheF = True


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(FPS)

    pygame.display.update()

pygame.quit()

if nv == 1:
    import Lvl1
elif nv == 2:
    import Lvl2
elif nv == 3:
    import Lvl3
elif nv == 4:
    import Lvl4
elif nv == 5:
    import Lvl5