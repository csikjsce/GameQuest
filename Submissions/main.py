import pygame

# Making a new window display in pygame.This is the base window.You need to pass a tuple to it
WIDTH,HEIGHT = 900,500
BG = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)

pygame.font.init()
pygame.mixer.init()

MAIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Justice Defence")
VELOCITY = 5

FPS = 60

HEALTH_FONT = pygame.font.SysFont('comicsans',32)
WINNER_FONT = pygame.font.SysFont('timesnewroman',100)

COWBOY = pygame.image.load('Assets/cowboy.png')  # (Xpos , Ypos, Width, Height)
COWBOY = pygame.transform.scale(COWBOY,(40,80))

#COWBOY = pygame.transform.rotate(COWBOY,-90)
DEMON = pygame.image.load('Assets/demon.png')  # (Xpos , Ypos, Width, Height)
DEMON = pygame.transform.scale(DEMON,(110,150))

DEMON_DYING = pygame.mixer.Sound('Assets/demon-slaughter.mp3')

SPACE = pygame.image.load('Assets/Tilesets/Tileset6.png')
SPACE = pygame.transform.scale(SPACE,(WIDTH,HEIGHT))

COWBOY_HIT = pygame.USEREVENT +1
DEMON_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH/2-3,0,6,HEIGHT)

BULL_VEL = 3
FIRES = 3

def draw(cowboy,demon, cowboy_bullets, demon_fire,DEMON_HEALTH,COWBOY_HEALTH):
    MAIN.blit(SPACE,(0,0))

    pygame.draw.rect(MAIN,BLACK,BORDER)

    demon_health = HEALTH_FONT.render("Health :",+str(DEMON_HEALTH),True,BLACK)
    cowboy_health = HEALTH_FONT.render("Health :",+str(COWBOY_HEALTH),True,BLACK)

    MAIN.blit(demon_health,(WIDTH - demon_health.get_width() - 10,10))
    MAIN.blit(cowboy_health,(10,10))

    MAIN.blit(COWBOY,(cowboy.x,cowboy.y))
    MAIN.blit(DEMON,(demon.x,demon.y))

    for bullets in cowboy_bullets:
        pygame.draw.rect(MAIN,YELLOW,bullets)

    for fires in demon_fire:
        pygame.draw.rect(MAIN,RED,fires)


    pygame.display.update()


def handle_cowboy_movement(keys_pressed,cowboy):
    if(keys_pressed[pygame.K_a]) and cowboy.x - VELOCITY > 0:
            cowboy.x -=VELOCITY

    if(keys_pressed[pygame.K_d]) and cowboy.x + VELOCITY + cowboy.width < BORDER.x:
        cowboy.x +=VELOCITY

    if(keys_pressed[pygame.K_w]) and cowboy.y - VELOCITY > 0 :
        cowboy.y -=VELOCITY

    if(keys_pressed[pygame.K_s]) and cowboy.y + VELOCITY + cowboy.height< HEIGHT:
        cowboy.y += VELOCITY

def handle_demon_movement(keys_pressed,demon):
    if(keys_pressed[pygame.K_LEFT] and demon.x-VELOCITY > BORDER.x + BORDER.width):
        demon.x -=VELOCITY

    if(keys_pressed[pygame.K_RIGHT]) and demon.x + VELOCITY + demon.width < WIDTH:
        demon.x +=VELOCITY

    if(keys_pressed[pygame.K_UP]) and demon.y -VELOCITY >0:
        demon.y -=VELOCITY

    if(keys_pressed[pygame.K_DOWN]) and demon.y + VELOCITY +demon.height<HEIGHT:
        demon.y += VELOCITY

def handle_bullets_and_fires(cowboy_bullets, demon_fires,cowboy,demon):
    for bullet in cowboy_bullets:
        bullet.x += BULL_VEL
        if demon.colliderect(bullet):
            pygame.event.post(pygame.event.Event(DEMON_HIT))
            cowboy_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            cowboy_bullets.remove(bullet)

    for bullet in demon_fires:
        bullet.x -= BULL_VEL
        if cowboy.colliderect(bullet):
            pygame.event.post(pygame.event.Event(COWBOY_HIT))
            demon_fires.remove(bullet)

        elif bullet.x < 0:
            demon_fires.remove(bullet)


def main():

    clock = pygame.time.Clock()
    running = True
    COWBOY_HEALTH = 5
    DEMON_HEALTH = 5
    demon_fires = []
    cowboy_bullets = []
    cowboy = pygame.Rect(100,300,40,80)
    demon = pygame.Rect(700,300,110,150)

    # Handles main game loop.This loop is for redrawing the window , updating scores,checking for collisions,etc.
    
    while running: 
        clock.tick(FPS)
        for event in pygame.event.get():      # Get a list of all the events
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    bullet = pygame.Rect(cowboy.x + cowboy.width,cowboy.y + cowboy.height//2-2, 10 ,5)   # -> Xpos , Ypos, Width and Heiht
                    cowboy_bullets.append(bullet)

                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(demon.x,demon.y + demon.height//2-4, 20 ,10)   # -> Xpos , Ypos, Width and Heiht
                    demon_fires.append(bullet)

            if event.type == DEMON_HIT:
                DEMON_HEALTH -=1
                DEMON_DYING.play()


            if event.type == COWBOY_HIT:
                COWBOY_HEALTH -=1

        winner_text = ""
        if DEMON_HEALTH <=0:
            winner_text = "Cowboy wins !"
        
        if COWBOY_HEALTH <=0:
            winner_text = "Demon wins!!"

        if(winner_text !=""):
            draw_text = WINNER_FONT.render(winner_text, True,(255,255,255))
            MAIN.blit(draw_text,(300,500))
            pygame.display.update()
            pygame.time.delay(5000)

        #print(cowboy_bullets,demon_fires)
        keys_pressed = pygame.key.get_pressed()   #  -> [False, False , True , ..... ]
        handle_cowboy_movement(keys_pressed,cowboy)
        handle_demon_movement(keys_pressed,demon)
        handle_bullets_and_fires(cowboy_bullets,demon_fires,cowboy,demon)

        draw(cowboy,demon,cowboy_bullets,demon_fires,DEMON_HEALTH,COWBOY_HEALTH)
        
    
    pygame.quit()


if __name__ == '__main__':
    main()