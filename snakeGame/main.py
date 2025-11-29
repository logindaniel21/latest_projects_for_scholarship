import pygame
from random import choice

pygame.init()
screen = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("SNAKE")

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 36)

snake_image = pygame.image.load("snake.png")

mango = pygame.image.load("mango.png")
mango = pygame.transform.scale(mango, (50,50))

background = pygame.image.load("background.png")

snake_x = 400
snake_y = 550

mango_x = choice(range(0, 950, 50))
mango_y = choice(range(0, 700, 50))

speed = 6.7 #grid units/s (100 pixels)

score = 0

class SNAKE:
    def __init__(self, x=500, y=350, length=0, posititons=None, snake_image=None):
        self.x = x
        self.y = y
        self.length = length
        self.positions = []

        self.rightside = self.x + 70
        self.leftside = self.x
        self.topside = self.y
        self.bottomside = self.y + 70

        if snake_image is None:
            snake_image = pygame.image.load("snake.png")
        self.snake_image_original = pygame.transform.scale(snake_image, (70,70))
        self.snake_image = pygame.transform.rotate(self.snake_image_original, 180)
    
    #Movement methods
    def up(self):
        self.y -= (speed*50)/60
        self.snake_image = pygame.transform.rotate(self.snake_image_original, 180)

    def down(self):
        self.y += (speed*50)/60
        self.snake_image = pygame.transform.rotate(self.snake_image_original, 0)

    def right(self):
        self.x += (speed*50)/60
        self.snake_image = pygame.transform.rotate(self.snake_image_original, 90)

    def left(self):
        self.x -= (speed*50)/60
        self.snake_image = pygame.transform.rotate(self.snake_image_original, -90)

    #body methods    
    def update_positions(self):
        # Add current head position to the front of the list
        self.positions.insert(0, [self.x, self.y])
        
        # Limit the list to the snake's length
        if len(self.positions) > self.length:
            self.positions = self.positions[:(self.length*5)]

    #Draw method
    def draw(self, x, y):
        # Draw the body segments
        for coord in self.positions:
            if state == "left":
                pygame.draw.circle(screen, (160,196,50), (coord[0]+45, coord[1]+15), 20)
            elif state == "right":
                pygame.draw.circle(screen, (160,196,50), (coord[0]+5, coord[1]+15), 20)
            elif state == "up":
                pygame.draw.circle(screen, (160,196,50), (coord[0]+25, coord[1]+35), 20)
            elif state == "down":
                pygame.draw.circle(screen, (160,196,50), (coord[0]+27, coord[1]+5), 20)
           

        screen.blit(self.snake_image, (self.x-9, self.y-19))

snake = SNAKE()

state = "stop"#   Default state#

def game_over():
    # Game over screen
    screen.fill("black")
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    final_score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))

    screen.blit(game_over_text, (screen.get_width()//2 - game_over_text.get_width()//2, 300))
    screen.blit(final_score_text, (screen.get_width()//2 - final_score_text.get_width()//2, 400))

    pygame.display.update()
    pygame.time.wait(5000)
    exit()

while True:
    for event in pygame.event.get(): #QUIT event handler
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        #Keypress event handling
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                if state != "down":
                    state = "up"
                else:
                     state = "down"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if state != "up":
                    state = "down"
                else:
                    state = "up"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if state != "left":
                    state = "right"
                else:
                    state = "left"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if state != "right":
                    state = "left"
                else:
                    state = "right"

    match state:    #more event handling 
        case "up":
            snake.up()
            snake.x = round(snake.x/50)*50
        case "down":
            snake.down()
            snake.x = round(snake.x/50)*50
        case "left":
            snake.left()
            snake.y = (round(snake.y/50)*50)+8
        case "right":
            snake.right()
            snake.y = (round(snake.y/50)*50)+8

        case "stop":
            pass
        case _:
            print("OHIO= Only Happens In Ohio")
            exit()

    #Collision handling
    if snake.x >= 965:
        game_over()
    elif snake.x < -15:
        game_over()
    elif snake.y < -15:
        game_over()
    elif snake.y > 725:
        game_over()

    #LATER ADD IF SNAKE COLLIDES W ITSELF GM

    
    if snake.x > mango_x - 50 and snake.x < mango_x + 50 and snake.y > mango_y - 40 and snake.y < mango_y + 50:
        mango_x = choice(range(0, 950, 50))
        mango_y = choice(range(0, 700, 50))
        snake.length += 1
        score += 1       
        speed += 0.4

    screen.fill("black")#   Clear frame
    screen.blit(background, (0,0))# Display bg

    screen.blit(mango, (mango_x, mango_y))#   display mango

    snake.draw(snake_x, snake_y)#   DIsplay snake

    text = font.render(f"Score: {score}", True, (255, 0, 0))
    screen.blit(text, (20,20))

    snake.update_positions()

    pygame.display.update()#    regular shi
    clock.tick(60)