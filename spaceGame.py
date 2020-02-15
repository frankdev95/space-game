import pygame
import random
import math

# Initalise pygame module
pygame.init()

# Game logic boolean
running = True

# Arrays used for holding the bullets and enemies.
bullets = []
enemies = []
counter = 0

# Player Class
class Player:

    xPos: int
    yPos: int 
    width: int
    height: int
    speed: int
    img = None
    bullet_fire = False
    
    # Initialises the class variables.
    def __init__(self, xPos, yPos, speed, path):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.img = pygame.image.load("player.png")
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    
    # Draws the player on the screen.
    def draw(self):
        screen.blit(self.img, (int(self.xPos), int(self.yPos)))
    
    # Moves the player based on key input events logged from the user.
    def move(self, event):
   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.xPos > 0:
                self.xPos -= self.speed
            if event.key == pygame.K_RIGHT and self.xPos < screen_width - self.width:
                self.xPos += 1
            if event.key == pygame.K_SPACE:
                self.bullet_fire = True
    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.bullet_fire = False
    
    # Getters
    def getxPos(self):
        return self.xPos
    
    def getyPos(self):
        return self.yPos
            
# Enemy Class
class Enemy:

    xPos: int
    yPos: int
    speed: int
    width: int
    height: int
    hit = 0
    img = None
    
    # Initialises the class variables.
    def __init__(self, xPos, yPos, speed, path):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.img = pygame.image.load(path)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
    
    # Draws the enemy onto the screen.
    def draw(self):
        screen.blit(self.img, (self.xPos, self.yPos))
    
    # Moves the enemies whilst checking if they hit the side, if so then reverses their direction.
    def move(self):
        self.xPos += self.speed
        if self.xPos >= (screen_width - self.width) or self.xPos <= 0:
            self.speed *= -1
            self.yPos += 30
    
    # Checks if the enemy is out of bounds on the y axis.
    def out_of_bounds(self):
        if self.yPos <= 0:
            return True
    
    # Keeps track of when a bullet hits the enemy.
    def addHit(self):
        self.hit += 1
    
    # Once the enemy is hit over or equal to 3 times, will returns true so it can be removed from the array.
    def isHit(self):
        if self.hit >= 3:
            return True
            
    # Getters and setters
    def setyPos(self, yPos):
        self.yPos += yPos
    
    def getxPos(self):
        return self.xPos
                
    def getyPos(self):
        return self.yPos

# Bullet Class        
class Bullet:
    
    xPos: int
    yPos: int
    speed: int
    bullet_state = "fire"
    collision = False
    img = None
    
    # Initialises the class variables.
    def __init__(self, xPos, yPos, speed, path):
        self.xPos = xPos
        self.yPos = yPos
        self.speed = speed
        self.img = pygame.image.load(path)
    
    # Checks if the bullet goes out of bounds on the y axis.
    def out_of_bounds(self):
        if self.yPos <= 0:
            return True
            
    # Draws the bullet onto the screen.
    def draw(self):
        if self.bullet_state == "fire":
            screen.blit(self.img, (int(self.xPos), int(self.yPos)))
    
    # Moves the bullets on the y axis.
    def move(self):
        self.yPos -= self.speed
    
    # Checks collision between the bullet and enemy, if they collide then returns true.
    def isCollision(self, x2, y2):
        distance = math.sqrt((math.pow(x2 - self.xPos, 2)) + (math.pow(y2 - self.yPos, 2)))
        if distance <= 50:
            return True
        else:
            return False

# Allows a specified number of initialised enemy objects to be appended into the enemy array.
def randEnemies(max_num):
    for enemy in range(0, max_num):
        rand_xPos = random.randint(0, screen_width - 100)
        rand_yPos = random.randint(0, screen_height / 3)
        rand_speed = random.randint(1, 2)
        rand_img = random.randint(1, 3)
        enemies.append(Enemy(rand_xPos, rand_yPos, rand_speed, f"monster{rand_img}.png"))
        
# Screen 
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))

# Score and Gameover text
score = pygame.font.SysFont("monospace", 16)
game_text = pygame.font.SysFont("monospace", 48)
points = 0

# Background
backgound = pygame.image.load("spacebg.jpg")

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
player = Player(screen_width / 2, screen_height - 100, 2, "player.png")

# Enemies
randEnemies(10)

# Game Loop
while running:
    
    # Draws the background and score onto the screen
    screen.blit(backgound, (0, 0))
    scoretext = score.render(f"Score: {points}", 1, (255, 255, 255))
    screen.blit(scoretext, (20, 20))
    
    # If the player quits the game, running will then equal false and the game loop ends.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Uses the player object methods to draw and move the player on the screen.
    player.draw()
    player.move(event)
    
    # Loops through each enemy in the enemies array, 
    # using their object methods to draw and move enemy on the screen.
    for enemy in enemies: 
        enemy.draw()
        enemy.move()
        # Checks if the enemy has been hit a specified number of times, if so removes the enemy from the array.
        if enemy.isHit():
            enemies.remove(enemy)
    
    # If the user is firing, takes advantage of the modulo operator to add bullets to an array. 
    if player.bullet_fire:
        counter += 1
        if counter % 50 == 0:
            bullets.append(Bullet(player.getxPos() + 16, player.getyPos() - 32, 5, "bullet.png"))
        
    # Loops through the bullets in the array, and if in firing state draw and moves onto the screen    
    for bullet in bullets:
        if bullet.bullet_state == "fire":
            bullet.draw()
            bullet.move()
            # Checks for any collision between enemies and bullets, adding to score board if hit,
            # and calls the addhit method which tracks the amount of times the enemy has been hit.
            for enemy in enemies:
                if bullet.isCollision(enemy.getxPos(), enemy.getyPos()):
                    points += 1
                    enemy.addHit()

    # Game over when the length of the enemey array reaches 0.
    if len(enemies) <= 0:
        print("game over!")
        running = False
        gameOver = True
        
    # Updates the display
    pygame.display.update()

# When game over is true then it shows the user their score    
while gameOver:

    screen.blit(backgound, (0,0))
    gameover_text = game_text.render(f"GAME OVER! Final Score: {points}", 1, (255, 255, 255))
    screen.blit(gameover_text, (110, screen_height / 2))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameOver = False
    
    pygame.display.update()
