import os
import sys
import pygame


pygame.init()



HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT+2

WIDTH=1500
HEIGHT=800

SPACE_WIDTH=70
SPACE_HEIGHT=60

BULLET_VEL=12
SPACE_SPEED=10

WINDOW_SCREEN=(WIDTH,HEIGHT)

wall=pygame.Rect(WIDTH/2-10,0,20,HEIGHT)


window =pygame.display.set_mode(WINDOW_SCREEN)

pygame.display.set_caption('Trial Game')

YELLOW_SPACE_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
RED_SPACE_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_red.png'))

BACKGROUND_IMAGE=pygame.image.load(os.path.join('Assets','space.png'))
background= pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))

YELLOW_SPACE=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACE_IMAGE,(SPACE_WIDTH,SPACE_HEIGHT)),90)
RED_SPACE=pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMAGE,(SPACE_WIDTH,SPACE_HEIGHT)),-90)

red_space=RED_SPACE.get_rect()

red_space.x=WIDTH-70
red_space.y=HEIGHT//2

yellow_space=YELLOW_SPACE.get_rect()
yellow_space.x=0
yellow_space.y=HEIGHT//2


def red_movement(keys_pressed,red_space):
    if keys_pressed[pygame.K_UP] and red_space.y>0:
        red_space.y -= SPACE_SPEED

    if keys_pressed[pygame.K_LEFT] and red_space.left > wall.right:
        red_space.x -=SPACE_SPEED

    if keys_pressed[pygame.K_RIGHT] and red_space.right < WIDTH:
        red_space.x += SPACE_SPEED

    if keys_pressed[pygame.K_DOWN] and red_space.bottom < HEIGHT:
        red_space.y += SPACE_SPEED


def yellow_movement(keys_pressed,yellow_space):
    if keys_pressed[pygame.K_w] and yellow_space.top > 0:
        yellow_space.y -= SPACE_SPEED

    if keys_pressed[pygame.K_a] and yellow_space.left > 0:
        yellow_space.x -=SPACE_SPEED

    if keys_pressed[pygame.K_d] and yellow_space.right < wall.left:
        yellow_space.x += SPACE_SPEED

    if keys_pressed[pygame.K_s] and yellow_space.bottom < HEIGHT:
        yellow_space.y += SPACE_SPEED


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def handle_bullets(red,red_bullets,yellow,yellow_bullets):
    if len(red_bullets) > 0:
        for bullet in red_bullets:
            bullet.x -= BULLET_VEL
            pygame.draw.ellipse(window, RED, bullet)        

            if bullet.x < 0:
                red_bullets.remove(bullet)
            elif yellow.colliderect(bullet):
                red_bullets.remove(bullet)
                pygame.event.post(pygame.event.Event(RED_HIT))
            else:
                for yellow_bullet in yellow_bullets:
                    if bullet.colliderect(yellow_bullet):
                        red_bullets.remove(bullet)
                        yellow_bullets.remove(yellow_bullet)
                        print("Bullet collision!")


    if len(yellow_bullets)>0:
        for bullet in yellow_bullets:
            bullet.x += BULLET_VEL
            pygame.draw.ellipse(window, YELLOW, bullet)

            if bullet.x > WIDTH:
                yellow_bullets.remove(bullet)
            elif red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                yellow_bullets.remove(bullet)
            else:
                for red_bullet in red_bullets:
                    if bullet.colliderect(red_bullet):
                        yellow_bullets.remove(bullet)
                        red_bullets.remove(red_bullet)
                        print("Bullet collision!")

def draw(red_health, yellow_health):
    red_health_text = HEALTH_FONT.render(
            "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
            "Health: " + str(yellow_health), 1, WHITE)
    window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    window.blit(yellow_health_text, (10, 10))


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    window.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
    # bullets store
    red_bullets=[]
    yellow_bullets=[]

    clock = pygame.time.Clock()

    # players health
    red_health = 10
    yellow_health = 10

    running=True
    while running:

        clock.tick(60)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RCTRL and len(red_bullets) <= 14:
                    bullet=pygame.Rect(red_space.x+red_space.width,red_space.y+red_space.height,10,10)
                    red_bullets.append(bullet)

                if event.key==pygame.K_LCTRL and len(yellow_bullets) <= 14:
                    bullet=pygame.Rect(yellow_space.x+yellow_space.width,yellow_space.y+yellow_space.height,10,10)
                    yellow_bullets.append(bullet)
            if event.type == RED_HIT:
                yellow_health -= 1

            if event.type == YELLOW_HIT:
                red_health -= 1

        # keys pressed 
        keys_pressed=pygame.key.get_pressed()

        #yellow moves
        yellow_movement(keys_pressed,yellow_space)

        #red moves 
        red_movement(keys_pressed,red_space)

        window.blit(background,(0,0))
        pygame.draw.rect(window,(0,0,0),wall)

        handle_bullets(red_space,red_bullets,yellow_space,yellow_bullets)


        winner_text=''
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        window.blit(YELLOW_SPACE,yellow_space)
        window.blit(RED_SPACE,red_space)
        draw(red_health,yellow_health)

        pygame.display.update()

    # Quit Pygame

    main()


if __name__ =="__main__":
    main()
