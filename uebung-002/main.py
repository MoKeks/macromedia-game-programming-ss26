import pygame


# ---- Bildschirm ----
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400



# ---- Farben (Rot, Grün, Blau, [Alpha]) ----
BACKGROUND_COL = (20, 100, 200)
GROUND_COL = (80, 70, 30)
PLAYER_COL = (30, 210, 76)
CIRCLE_COL = (200, 200, 255)
TEXT_COL = (255, 255, 255)
BLACK = (0, 0, 0)

# ---- pygame starten ----
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jump & Run")
clock = pygame.time.Clock()

# ---- Player ----
player_x = 100.0
player_y = 100.0
player_radius = 20
player_moving_left = False
player_moving_right = False
player_movement_y = 0
player_gravity = 0.1

jump_sound = pygame.mixer.Sound("sounds/jump.wav")

player = pygame.image.load("cat_sprite.png")


# ---- Bouncing circle (aus dem "Boing boing"-Beispiel) ----

circle_x = 300
circle_y = 50
circle_radius = 10
circle_movement_x = 1.0
circle_movement_y = 0.0
gravity = 0.1



# ---- Obstacles (Boden + Plattformen) ----
# Jedes Obstacle ist ein pygame.Rect(x, y, breite, hoehe)
obstacles = []

# Boden
obstacles.append( pygame.Rect(0, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 10))

# Plattformen
obstacles.append( pygame.Rect(200, SCREEN_HEIGHT - 60, 200, 10))

obstacles.append( pygame.Rect(400, SCREEN_HEIGHT - 125, 100, 10))

obstacles.append( pygame.Rect(120, SCREEN_HEIGHT - 250, 80, 10))

obstacles.append( pygame.Rect(250, SCREEN_HEIGHT - 150, 50, 10))

obstacles.append( pygame.Rect(350, SCREEN_HEIGHT - 200, 100, 10))

# Kugeln zum sammeln

#für spawntime
last_event_time = pygame.time.get_ticks()
event_interval = 3000  # in Millisekunden = 5 Sekunden


reward_count = 1

rewards = []

score = 0

# playtime
time = pygame.time.get_ticks()


# ---- Functions ----
def SetGrav(active):
    #print(active)
    global player_gravity
    if active:
        player_gravity = 0.1
        #print("grav on")
    if active==False:
        #print ("grav off")
        player_gravity = 0



# ============================================================
# Game Loop
# ============================================================

running = True
while running:

    

    # ---- Events ----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_moving_left = True
            elif event.key == pygame.K_d:
                player_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_moving_left = False
            elif event.key == pygame.K_d:
                player_moving_right = False

    # ---- Update ----
    
    if time < 30000 :
        time = pygame.time.get_ticks()
        # Player-Bewegung
        if player_moving_right:
            player_x += 3
        elif player_moving_left:
            player_x -= 3

     # Player: Gravitation
        player_movement_y += player_gravity
        player_y += player_movement_y

        

        # Bouncing circle: Gravitation + Bewegung
        circle_movement_y += gravity
        circle_x += circle_movement_x
        circle_y += circle_movement_y

        # Bouncing circle: Am Boden abprallen
        if circle_y >= SCREEN_HEIGHT - 20 - circle_radius:
            circle_movement_y = -circle_movement_y

        # Bouncing circle: An den Seiten abprallen
        if circle_x <= circle_radius or circle_x >= SCREEN_WIDTH - circle_radius:
            circle_movement_x = -circle_movement_x

        # Collision
        player_collider = pygame.Rect (player_x , player_y, player_radius, player_radius)
        
        #Rewards spawnen
        current_time = pygame.time.get_ticks()
        if current_time - last_event_time >= event_interval:
            last_event_time = current_time
            if reward_count == 1:
                reward_count += 1
                rewards.append( pygame.Rect(100, 0, 10, 10))
            elif reward_count == 2:
                reward_count += 1
                rewards.append( pygame.Rect(350, 0, 10, 10))
            elif reward_count == 3:
                reward_count += 1
                rewards.append( pygame.Rect(200, 0, 10, 10))
            elif reward_count == 4:
                reward_count = 1
                rewards.append( pygame.Rect(50, 0, 10, 10))
            elif reward_count == 5:
                reward_count += 1
                rewards.append( pygame.Rect(175, 0, 10, 10))
            elif reward_count == 6:
                reward_count == 1
                rewards.append( pygame.Rect(250, 0, 10, 10))


        # rewards gravitation
        for reward in rewards:
            reward.y += 2

        #rewards sammeln
        collected_rewards = player_collider.collidelistall(rewards)
        if collected_rewards:
            score += len(collected_rewards)
            for i in sorted(collected_rewards, reverse=True):
                del rewards[i]

        # rewards collision
        rewards = [reward for reward in rewards if reward.collidelist(obstacles) == -1]


        if player_collider.collidelistall (obstacles) :
            #player_gravity = 0
            SetGrav(False)
            player_movement_y = 0
            

            # Jump
            keys = pygame.key.get_pressed()
            if keys [pygame.K_SPACE]:
                #player_gravity = 0.1
                SetGrav(True)
                print("jump")
                jump_sound.play()
                player_movement_y -= 5
                
        else :
            SetGrav(True)
            #player_gravity = 0.1

            #print("no collide")

        # ---- Status-Text ----
        bouncing_circle = pygame.Rect (circle_x, circle_y, circle_y, circle_radius)
    
        if player_collider.colliderect (bouncing_circle):
            status = "Ouch!"
            print ("Ouch")
        else:
            status = "Wheee!"

        # ---- Draw ----
        screen.fill(BACKGROUND_COL)

        # Obstacles zeichnen
        for obs in obstacles:
            pygame.draw.rect(screen, GROUND_COL, obs)

        # Bouncing circle zeichnen
        pygame.draw.circle(screen, CIRCLE_COL, (int(circle_x), int(circle_y)), circle_radius)

        # Player zeichnen
        player_rect = player.get_rect(center=(int(player_x), int(player_y)))
        screen.blit(player, player_rect)
        # Text zeichnen
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(f"{status}", True, TEXT_COL)
        screen.blit(text_surface, (30, 30))

        font = pygame.font.SysFont(None, 40)
        text_surface = font.render(f"Score: {score}", True, TEXT_COL)
        screen.blit(text_surface, (400, 30))

        # Rewards Zeichnen
        for reward in rewards:
            pygame.draw.circle(screen, (250, 0, 0), reward.center, 5)

    else:
        print ("playtime over")
        #Nach ablauf der playtime score zeigen
        screen.fill (BLACK)
        font = pygame.font.SysFont(None, 80)
        text_surface = font.render(f"Final Score: {score}", True, TEXT_COL)
        screen.blit(text_surface, (110, 180))


    # ---- Flip ----
    pygame.display.flip()
    clock.tick(60)

pygame.quit()