import pygame
from pygame import mixer

pygame.init()

#load music
mixer.init()
mixer.music.load("data/Game.wav")
mixer.music.set_volume(1)
mixer.music.play(-1)
jump = pygame.mixer.Sound('data/jump.wav')
jump.set_volume(0.07)
go = pygame.mixer.Sound('data/gameover.wav')
go.set_volume(0.2)

clock = pygame.time.Clock()
FPS = 30

screen_width = 650
screen_height = 650

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SwordOfOrion - Level 3')

tile_size = 25
rapport = int(screen_height/tile_size)

game_over = 0
main_menu = True

bg = pygame.image.load('data/background.jpg')
restart_img = pygame.image.load('data/restartButton.png')
triangle_temp = pygame.image.load('data/triangle3.png')
triangle = pygame.transform.scale(triangle_temp, (30, 30))

myfont = pygame.font.Font("data/future.ttf", 30)
exit = myfont.render("exit", 1, (255, 255, 255))
restart = myfont.render("restart", 1, (255, 255, 255))
next = myfont.render("next level", 1, (255, 255, 255))

myfont2 = pygame.font.Font("data/future.ttf", 30)
lvl = myfont2.render("Lvl 3", 1, (255, 255, 255))

myfont3 = pygame.font.Font("data/future.ttf", 75)
image_texte = myfont3.render("GAME OVER", 1, (255, 255, 255))


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5

        if game_over == 0:
            # get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                jump.play()
                self.vel_y = -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= self.velocity
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += self.velocity
                self.counter += 1
                self.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # add gravity
            self.vel_y += 1
            if self.vel_y > 20:
                self.vel_y = 20
            dy += self.vel_y

            # check for collision
            self.in_air = True
            for tile in world.tile_list:
                # check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

        # check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                go.play()
                game_over = -1

            # check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                go.play()
                game_over = -1

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > -100:
                self.rect.y -= 7

        # draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.velocity = 3
        for num in range(1, 3):
            img_right = pygame.image.load(f'data/player{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 50))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        dead_image = pygame.image.load('data/ghost.png')
        self.dead_image = pygame.transform.scale(dead_image, (40, 40))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = False

class World():
    def __init__(self, data):
        self.tile_list = []

        #load images
        blackStone = pygame.image.load('data/stoneTile2.png')
        stone = pygame.image.load('data/stoneTile3.png')
        lavaimg = pygame.image.load('data/lavaTile.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(blackStone, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(stone, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size - 5)
                    blob_group.add(blob)
                if tile == 4:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 5:
                    exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit)
                if tile == 6:
                    img = pygame.transform.scale(lavaimg, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image_temp = pygame.image.load('data/goomba.png')
        self.image = pygame.transform.scale(self.image_temp, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 3
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 3
        if abs(self.move_counter) > 170:
            self.move_direction *= -1
            self.move_counter *= -1

class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/lavaTile.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('data/door.png')
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 4, 4, 2, 2, 4, 4, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


player = Player(100, screen_height - 50)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World(world_data)

tours = 0
endroit = "restart"
endroit2 = "next"
nvsuiv = False

run = True
while run:

    clock.tick(FPS)

    screen.blit(bg, (0, 0))  # affiche le backgroung
    screen.blit(lvl, (550, 35))

    world.draw() # dessine le decor

    if game_over == 0:
        blob_group.update() # update des mobs

    lava_group.draw(screen)
    blob_group.draw(screen)
    exit_group.draw(screen)

    game_over = player.update(game_over)

    game_over = player.update(game_over)

    # if player has died
    key = pygame.key.get_pressed()
    if game_over == -1:
        screen.blit(restart, (200, 350))
        screen.blit(exit, (400, 350))
        screen.blit(image_texte, (screen_width // 2 - 175, screen_height // 2 - 50))
        if endroit == "restart":
            screen.blit(triangle, (160, 345))
        else:
            screen.blit(triangle, (360, 345))
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and endroit == "restart":
            endroit = "exit"
        if key[pygame.K_LEFT] and endroit == "exit":
            endroit = "restart"
        if key[pygame.K_RETURN] and endroit == "restart":
            player.reset(100, screen_height - 50)
            game_over = 0
        elif key[pygame.K_RETURN] and endroit == "exit":
            run = False

    if game_over == 1:
        screen.blit(next, (200, 350))
        screen.blit(exit, (400, 350))
        if endroit2 == "next":
            screen.blit(triangle, (160, 345))
        else:
            screen.blit(triangle, (360, 345))
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and endroit2 == "next":
            endroit2 = "exit"
        if key[pygame.K_LEFT] and endroit2 == "exit":
            endroit2 = "next"
        if key[pygame.K_RETURN] and endroit2 == "next":
            nvsuiv = True
            run = False
        elif key[pygame.K_RETURN] and endroit2 == "exit":
            run = False
        file = open("data/Sauvegarde.txt", "r")
        l = file.readlines()
        file.close()
        l[2] = "3=OO\n"
        l[3] = "4=ON\n"
        file = open("data/Sauvegarde.txt", "w")
        file.writelines(l)
        file.close()
        player.rect.x = 1000
        myfont = pygame.font.Font("data/future.ttf", 40)
        image_texte = myfont.render("LEVEL COMPLETED", 1, (255, 255, 255))
        screen.blit(image_texte, (screen_width - 480 , screen_height // 2 - 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()

if nvsuiv == True:
    pass
    import Lvl4