import time
import pygame
from pygame import mixer

pygame.init()

clock = pygame.time.Clock()
FPS = 30

screen_width = 800
screen_height = 560

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SwordOfOrion - Menu')


#load images
bg_img = pygame.image.load('data/menuBackGround.jpg')
logo_temp = pygame.image.load('data/logo.png')
logo = pygame.transform.scale(logo_temp, (500, 410))
triangle_temp = pygame.image.load('data/triangle.png')
triangle = pygame.transform.scale(triangle_temp, (50, 50))

#load textes
myfont = pygame.font.Font("data/future.ttf", 50)
play_text = myfont.render("PLAY", 1, (0, 0, 0))
exit_text = myfont.render("EXIT", 1, (0, 0, 0))
reboot_text = myfont.render("REBOOT", 1, (0, 0, 0))

#load music
mixer.init()
mixer.music.load("data/Menu.wav")
mixer.music.set_volume(0.6)
mixer.music.play(-1)
ok = pygame.mixer.Sound('data/okBtn.wav')
select = pygame.mixer.Sound('data/selectBtn.wav')

#define variables
endroit = "play"
image = True
tours = 0
y = 270
menu_niv = False
toucheU = True
toucheD = False

run = True
while run:
    tours += 1

    screen.blit(bg_img, (0, 0))
    screen.blit(logo, (150, -75))
    screen.blit(play_text, (350, 275))
    screen.blit(exit_text, (350, 325))
    screen.blit(reboot_text, (350, 375))

    if tours%15 == 0:
        if image == True:
            image = False
        else:
            image = True

    if image == True:
        screen.blit(triangle, (290, y))

    key = pygame.key.get_pressed()
    if key[pygame.K_DOWN] and endroit == "play" and toucheD == True:
        select.play()
        toucheD = False
        endroit = "exit"
        y = 320
    elif key[pygame.K_DOWN] and endroit == "exit" and toucheD == True:
        select.play()
        toucheD = False
        endroit = "reboot"
        y = 370

    if key[pygame.K_UP] and endroit == "reboot"and toucheU == True:
        select.play()
        toucheU = False
        endroit = "exit"
        y = 320
    if key[pygame.K_UP] and endroit == "exit" and toucheU == True:
        select.play()
        toucheU = False
        endroit = "play"
        y = 270

    if tours % 15 == 0 and toucheU == False:
        toucheU = True

    if tours % 15 == 0 and toucheD == False:
        toucheD = True

    if key[pygame.K_RETURN]:
        ok.play()
        time.sleep(0.3)
        if endroit == "exit":
            run = False
        elif endroit == "play":
            menu_niv = True
            run = False
        elif endroit == "reboot":
            file = open("data/Sauvegarde.txt", "r")
            l = file.readlines()
            file.close()
            l[0] = "1=ON\n"
            l[1] = "2=NN\n"
            l[2] = "3=NN\n"
            l[3] = "4=NN\n"
            l[4] = "5=NN\n"
            file = open("data/Sauvegarde.txt", "w")
            file.writelines(l)
            file.close()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    clock.tick(FPS)

    pygame.display.update()

pygame.quit()

if menu_niv == True:
    import MenuNiv
