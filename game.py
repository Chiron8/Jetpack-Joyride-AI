import pygame
import random

# Setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

distance = 1
counter = 0
speed = 10

class Player:
    def __init__(self):
        self.run = pygame.image.load("Assets/player/run 1.png")
        self.fly = pygame.image.load("Assets/player/fly 1.png")
        self.land = pygame.image.load("Assets/player/land.png")
        self.pos = pygame.Vector2(screen.get_width() / 8 + 100, screen.get_height() / 2)
        self.dtn = 0
        self.rect = self.run.get_rect(topleft=(self.pos.x, self.pos.y))

    def update(self, keys):
        # Movement logic
        if keys[pygame.K_SPACE]:
            screen.blit(self.fly, (self.pos.x, self.pos.y))
            self.pos.y -= self.dtn + 0.2
            if self.dtn < 30:
                self.dtn += 0.7 
                screen.blit(self.land, (self.pos.x, self.pos.y))
            else:
                screen.blit(self.run, (self.pos.x, self.pos.y))
            if self.dtn > -30:
                self.dtn -= 0.7
            self.pos.y -= self.dtn

        self.rect.topleft = (self.pos.x, self.pos.y)  # Hitbox
        #pygame.draw.rect(screen, (0, 255, 0), self.rect)
        
        # Boundary constraints
        if self.pos.y > screen.get_height() / 10 * 8:
            self.pos.y = screen.get_height() / 10 * 8
            self.dtn = 0
        elif self.pos.y < screen.get_height() / 20:
            self.pos.y = screen.get_height() / 20          
            self.dtn = 0   

class Obstacle:
    def __init__(self):
        self.image = pygame.image.load("Assets/obstacles/Zapper.png")
        self.image = pygame.transform.scale_by(self.image, 0.3)
        self.pos = pygame.Vector2(screen.get_width(), 500)
        self.angles = [0, 45, 135, 90]
        self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))

    def update(self):
        global speed
        screen.blit(self.image, (self.pos.x, self.pos.y))
        self.pos.x -= speed
        self.rect.topleft = (self.pos.x, self.pos.y)

        # Respawn the obstacle after it goes off-screen
        if self.pos.x < -self.image.get_width():
            angle = random.choice(self.angles)
            self.image = pygame.image.load("Assets/obstacles/Zapper.png")  # Reset image to avoid stacking rotations
            self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
            self.rect = pygame.transform.rotate(self.rect, angle)
            self.image = pygame.transform.rotate(self.image, angle)
            self.pos.x = screen.get_width() * 1.2
            self.pos.y = random.randint(100, round(screen.get_height() * 0.8))
            self.rect = self.image.get_rect(topleft=(self.pos.x, self.pos.y))
            
        pygame.draw.rect(screen, (255, 0, 0), self.image.get_rect(topleft=(self.pos.x, self.pos.y)))

def game_loop():
    global distance, counter, speed

    player = Player()
    obstacle = Obstacle()
    running = True

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        screen.fill("dark gray")

        # Update and render player
        player.update(keys)

        # Update and render obstacle
        obstacle.update()


        # Collision detection
        if player.rect.colliderect(obstacle.rect):
            font = pygame.font.SysFont("Calibri", 100)
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2,
                                         screen.get_height() // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Pause for 2 seconds before quitting
            running = False

        # Render distance text
        font = pygame.font.SysFont("Calibri", 50)
        txtsurf = font.render("Distance: " + str(distance), True, (0, 0, 0))
        screen.blit(txtsurf, (175 - txtsurf.get_width() // 2, 100 - txtsurf.get_height() // 2))

        pygame.display.flip()
        clock.tick(60)

        # Increment distance and adjust speed
        if counter < 4:
            counter += speed / 20
        else:
            distance += 1
            counter = 0
            if distance % 100 == 0:
                speed *= 2

    pygame.quit()

game_loop()