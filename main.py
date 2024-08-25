import pygame
pygame.init()
import random
import pygame_menu
import math
import os

background_image = pygame.image.load('background.png')  
background_image = pygame.transform.scale(background_image, (500, 600))

font = pygame.font.Font(None, 36)
high_score = 0
# створення головного вікна
window_size = (500, 600)
window = pygame.display.set_mode((window_size))



class Player:
    def __init__(self, x, y, width, height, image):
        self.original_image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.original_image, (width, height))  # Зміна розміру зображення
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.gravity = 0.5
        self.jump_power = -10
        self.vel_y = 0
        self.can_jump = False
        self.jumps = 2
        self.score = 0

    def move(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for w in walls:
            if self.rect.colliderect(w.rect):              
                self.jumps = 2
                self.score +=  1 
                
                if self.vel_y > 0:
                    self.rect.bottom = w.rect.top
                    self.vel_y = 0
                    self.can_jump = True
                # elif self.vel_y < 0:
                #     self.rect.top = w.rect.bottom
                #     self.vel_y = 0

    def jump(self):
        if self.can_jump:
            self.vel_y = self.jump_power
            if self.jumps <= 1:     
                self.can_jump = False
            self.jumps -= 1 

    def move_horizontal(self, dx):
        self.jumps = 2
        self.rect.x += dx
        # for wall in walls:
        #     if self.rect.colliderect(wall.rect): 
        #         if dx > 0:
        #             self.rect.right = wall.rect.left
        #             self.vel_y = 0.1

        #         elif dx < 0:
        #             self.rect.left = wall.rect.right  
        #             self.vel_y = 0.1


class Wall:
    def __init__(self, x, y, width, height, color=(22, 26, 31)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)



# створення персонажа
player = Player(100, 100, 50, 50, 'player.png')

# створення стін
walls = [
    Wall(20, 100, 200, 1000),
    Wall(350, 100, 150, 400),
    Wall(100, 450, 500, 400),
]


if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

def start_game():
    global high_score
    # кольори
    white = (255, 255, 255)

    # створення об'єкту "годинник" для встановлення частоти кадрів
    clock = pygame.time.Clock()

    # головний цикл гри
    game = True
    move_left = False
    move_right = False

    pygame.mixer.music.load('background_music.wav')
    pygame.mixer.music.play(-1)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    move_right = True
                    player.original_image = pygame.image.load("player-reverse.png")
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_a:
                    move_left = True
                    player.original_image = pygame.image.load("player.png")
                    player.image = pygame.transform.scale(player.original_image, (50, 50))
                if event.key == pygame.K_w:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_a:
                    move_left = False

        window.blit(background_image, (0, 0))
        player.move()

        if move_right:
            player.move_horizontal(3)
        if move_left:
            player.move_horizontal(-3)

        for wall in walls:
            wall.draw(window)
            wall.rect.y += 1

        if player.score > high_score:
            high_score = player.score

        text = font.render(f"Рахунок: {player.score}", True, (255,0,0))
        text2 = font.render(f"Мій Рахунок: {high_score}", True, (255,0,0))

        window.blit(player.image, (player.rect.x, player.rect.y))
    

        if len(walls) < 8:
            if random.randint(1,450) % 147 == 0 :
                walls.append(Wall(random.randint(0,400),0,70,10))
        if len(walls) < 8:
            if random.randint(1,420) % 147 == 0:
                walls.append(Wall(random.randint(0,400),0,100,10))
        for w in walls:
            if w.rect.y >= 820:
                walls.remove(w)

        
        # if random.randint(1,1500) % 147 == 0:
        #     walls.append(Wall(random.randint(0,400),0,70,10))
        # if random.randint(1,1200) % 147 == 0:
        #     walls.append(Wall(random.randint(0,400),0,130,10))

        with open ("score.txt", "w") as file:
            file.write(str(high_score))
        window.blit(text2,(10,50))
        window.blit(text,(10,10))

        clock.tick(60)
        pygame.display.update()

    pygame.quit()
    pygame.mixer.music.stop()



def main_menu():
    menu = pygame_menu.Menu('Main Menu', *window_size, theme=pygame_menu.themes.THEME_GREEN)
    menu.add.button('Start Game', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        menu.update(events)
        menu.draw(window)
        pygame.display.update()

if __name__ == "__main__":
    main_menu()