# main.py
# Game loop for RealFakeGame.
#
# Controls:
#   Mouse X  — move player left/right
#   ESC      — quit
#   SPACE    — continue/restart (only in Shop/GameOver)
#
# This skeleton provides:
#   - Player that follows mouse and auto-fires shots
#   - Level with background image
#   - Parsed (but inactive) enemies and obstacles

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK
from player import Player
from level import Level
from gamestate import Game
from enemy import Enemy
from obstacle import Obstacle
from shot import Shot
from boss import Boss
from shop import Shop
from gameover import Gameover
from title import Title

from time import sleep

LEVEL_FILES = ["lvl001.rfg", "lvl002.rfg", "lvl003.rfg"]
#        Index       0           1              2         
# Macht es scaleable

def main():
    # ------------------------------------------------------------------ #
    #  Initialize pygame                                                 #
    # ------------------------------------------------------------------ #
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("RealFakeGame")
    clock = pygame.time.Clock()

    # ------------------------------------------------------------------ #
    #  Setup — create player and load level (ofApp::setup)   #
    # ------------------------------------------------------------------ #
    player = Player()
    player.setup(
        x=SCREEN_WIDTH // 2,           # Center of screen
        y=SCREEN_HEIGHT - 50,           # Near bottom of screen
        dx=0,
        dy=0,
        image_prefix="player_stage",
        anim_speed=1,
        hp=100,
    )
    player.set_might(rng= 500, dmg=5, cad=20, shotspd= 10)
    
    current_level = 0

    enemies = Enemy ()
    enemies.setup(
        x=SCREEN_WIDTH // 2,
        y=SCREEN_HEIGHT,
        dx=0,
        dy=0,
        image_prefix="enemy",
        anim_speed=1,
        hp=5 + 5 *current_level , #hp scalen mit lvl
    )

    shop = Shop()

    gameover = Gameover ()

    title = Title ()

    level = Level()
    level.load(LEVEL_FILES[current_level])
    

    duration = 0

    game_state = Game()
    game_state.change_state("title")

    points = 0
    highscore = 0
    old_highscore = highscore

    buff_duration = 0
    
    obstacle = Obstacle ()

    shot = Shot ()

    frame_stop = 0

    # ------------------------------------------------------------------ #
    #  Game loop                                                         #
    # ------------------------------------------------------------------ #
    running = True
    while running:
        dt= clock.tick(FPS)
            
            # -------------------------------------------------------------- #
            #  Event handling                                                 #
            # -------------------------------------------------------------- #
        for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     running = False
                 elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                     running = False
                    if event.key == pygame.K_SPACE:
                        if game_state.state == "gameover":
                            level, points, highscore, old_highscore, current_level = restart (player, enemies, level, game_state, highscore, old_highscore, current_level)
                            duration = 0
                        if game_state.state == "shop":
                            current_level, level = next_level(current_level, level, game_state)
                            duration = 0   
                        if game_state.state == "title":
                            game_state.change_state("playing")
                 elif event.type == pygame.MOUSEBUTTONDOWN:
                    if game_state.state == "shop":
                        points = shop.handle_click(event.pos, player, points) 
                        print ("Points:",points) #DEBUG       
                                    
            
                
                     
        if frame_stop > 0 :
            frame_stop -= 1
            continue

        # -------------------------------------------------------------- #
        #  Update                                                        #
        # -------------------------------------------------------------- #
          # checking for game-state
        if game_state.state == "playing":
            player.step()
            level.step()
            duration += 1
            for enemies in level.enemies:
                enemies.step(target_pos= player.pos, speed = enemies.speed)

       


          #----------------------------------------------------------------#
         # Check collisions
            #----------------------------------------------------------------#

         # Obstacle collsion
         # NOTE: Der typo ist wichtig 
            for obstacle in level.obstacles:
                 if obstacle.collsion(player.get_rect()):
                    obstacle.hp = 0  # kill the object
                    obstacle.is_alive ()
                    points += 200
                    buff_duration = 100
                    player.buff (True)
                    print ("buff start")

                 
          
          # Enemy collision
            for enemies in level.enemies:
                if not enemies.alive :
                    continue

                if enemies.collision(player.get_rect()):
                    player.hp -= enemies.damage     #nicht hard coden sonst sind die Werte aus der level.rfg irrelevant
                    print ("Damage Taken:", enemies.damage)
                    enemies.hp -= 10
                    enemies.is_alive()
                    points +=  50

                for shot in player.shots :
                    if enemies.collision(shot.get_rect()):
                        enemies.hp -= shot.dmg
                        enemies.is_alive()
                        shot.life = 0
                        #shot.is_alive ()
                        points += 100
                        break

                for obstacle in level.obstacles:
                    if obstacle.collsion (enemies.get_rect()):
                        direction = player.pos - enemies.pos
                        if direction.length() > 0:
                            direction = direction.normalize()
                        enemies.pos -= direction * 3                    
                    
                        
                
            
                       
             # Shot Collision

            # Buff Check
            # NOTE: Buffs dürfen sich nicht überlappen
            if buff_duration > 0 :
                buff_duration -= 1
                if buff_duration == 0:
                    player.buff (False)
                    print ("buff end")

             # Level Duration
            print ("Level Frame:", duration)            #DEBUG
            print ("Max Frames:", level.duration)       #DEBUG
            if level.duration == duration:            
                boss = spawn_Boss (current_level, level)


            # Game State Check (to shop und gameover)
            if player.hp <= 0 or current_level >= len(LEVEL_FILES):
                if points > highscore : #highscore checken
                    old_highscore = highscore
                    highscore = points
                game_state.change_state("gameover")
                frame_stop += 10
                continue
             #NOTE: es darf nur ein neuer State zugewiesen werden
            elif level.duration + 1 < duration:     #elif da sonst die game states sich gegenseitig aufheben#
                print ("Current HP:", boss.hp)          #DEBUG
        
                if boss.hp <= 0:            # der boss kann unter 0 hp fallen
                    # Beenden von Buff, falls noch aktiv
                    if buff_duration > 0:
                        buff_duration = 0
                        player.buff (False)
                        print ("buff end")
                    # Ins den shop gehen
                    game_state.change_state("shop")
                    frame_stop += 10
                    continue
                    
            
           
        ###########################################################
        ## game over mechanic
        ###########################################################

        elif game_state.state == "gameover":
           # wäre funny: pygame.quit # einfach spiel schließen wenn man stirbt
            #screen.fill(BLACK)
            print ("game over")

            
                
            # print ("space") #DEBUG

            # continue   # Spiellogik überspringen ## War wichtig bevor draw an die state machine gebunden wurde

        #######################################################
        # #Shop zwischen leveln
        ##########################################################
        elif game_state.state == "shop":
            if current_level >= len(LEVEL_FILES)-1:
                current_level, level = next_level(current_level, level, game_state)
                continue #draw wird übersprungen damit es nahtlos in game_over
            
            # Shop öffnen
            shop.shop_start ()

            #continue #rest nicht ausführen ## War wichtig bevor draw an die state machine gebunden wurde
            

        # -------------------------------------------------------------- #
        #  Draw                                                          #
        # -------------------------------------------------------------- #
       
       #### Wird immer gezeichnet
        screen.fill(BLACK)

        # Draw level background first
        level.draw(screen)
        # Draw enemies
        for enemies in level.enemies:
                enemies.draw(screen)
        # Draw obstacles
        for obstacle in level.obstacles:
                obstacle.draw(screen)
        # Draw player (also draws its shots internally)
        player.draw(screen)
        

        #state machine bpound drawing
        #draw title
        if game_state.state == "title":
            dim_screen(screen)
            title.draw_title (screen, SCREEN_WIDTH, SCREEN_HEIGHT)
        #draw playing
        if game_state.state == "playing":  
                    
            # HP Bar
            # hp = player.hp
            # print (hp) #DEBUG
            font = pygame.font.SysFont(None, 50)
            text = font.render(f"HP: {player.hp}/100", True, (255, 80, 80))
            screen.blit(text, (SCREEN_WIDTH - 230 , SCREEN_HEIGHT - 70))

            # Score system
            font = pygame.font.SysFont(None, 50)
            text = font.render(f"Score: {points}", True, (150, 50, 200))
            screen.blit(text, (SCREEN_WIDTH - 550 , SCREEN_HEIGHT - 750))

            font = pygame.font.SysFont(None, 30)
            text = font.render(f"Highscore: {old_highscore}", True, (150, 50, 200))
            screen.blit(text, (SCREEN_WIDTH - 550 , SCREEN_HEIGHT - 710))
       
       # Draw game over
        elif game_state.state == "gameover":
            dim_screen(screen)
            gameover.draw_gameover (screen, SCREEN_WIDTH, SCREEN_HEIGHT, points, highscore, old_highscore, current_level, LEVEL_FILES)
       
       #Draw Shop
        elif game_state.state == "shop":
            dim_screen(screen) # Setz den letzten state des Ganeplay als gedimmten Background
            shop.draw_shop (screen, SCREEN_WIDTH, SCREEN_HEIGHT, player, points)


        
        pygame.display.flip()
        clock.tick(FPS)

    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()

def restart (player, enemies, level, game_state, highscore, old_highscore, current_level):
    ### RESTART Funktion
    print ("RESTART")
    ## Player RESET
    player.setup(
    x=SCREEN_WIDTH // 2,           # Center of screen
    y=SCREEN_HEIGHT - 50,           # Near bottom of screen
    dx=0,
    dy=0,
    image_prefix="player_stage",
    anim_speed=1,
    hp=100,
    )
    #Stats RESET
    player.set_might(rng= 500, dmg=1, cad=20, shotspd= 10)
    #Enemy RESET
    enemies.setup(
    x=SCREEN_WIDTH // 2,
    y=SCREEN_HEIGHT,
    dx=0,
    dy=0,
    image_prefix="enemy",
    anim_speed=1,
    hp=10,
    )
    #level RESET
    current_level = 0
    level = Level()
    level.load(LEVEL_FILES[current_level])
    #point RESET
    global points
    points = 0
    if highscore > old_highscore: ##Saving Highscore
        old_highscore = highscore  
    game_state.change_state("playing")
    return level, 0 , highscore, old_highscore, current_level

def spawn_Boss (current_level, level):
   boss = Boss ()
   boss.setup ( 
        x=SCREEN_WIDTH // 2,
        y= 50,
        dx=1,
        dy=1,
        image_prefix="enemy",
        anim_speed=1,
        hp= 75 + current_level*50,
        damage= 5 + 5*current_level,
        speed = 15 + 3 * current_level,
        scale= float(3 + 2*current_level)
    )
   level.enemies.append(boss)
   print ("Boss Spwaned HP:", boss.hp) #DEBUG
   return boss

def dim_screen (screen):
    # Funktion um den den Bildschirm zu verdunkeln
    overlay = pygame.Surface(screen.get_size())
    overlay.fill (BLACK)
    overlay.set_alpha(180)

    screen.blit (overlay, (0 , 0))


def next_level(current_level, level, game_state):
    current_level += 1

    if current_level >= len(LEVEL_FILES):
      print("Kein weiteres Level mehr")
      game_state.change_state("playing")    
      #zurück in playing setzen da man aus "Shop kommt" aberdie game over transition in "playing" passiert (Damit der Highscore gesaved wird)
      return current_level, level   
    level = Level()
    level.load(LEVEL_FILES[current_level])
    game_state.change_state("playing")
    return current_level, level


# def  next_level (current_level) :
#     current_level =+ 1
#     if current_level == 1:
#         level = Level ()
#         level.load("lvl002.rfg")
#     if current_level == 2:
#         level = Level ()
#         level.load("lvl003.rfg")      
#     if current_level >= 3 :
#         return 


if __name__ == "__main__":
    main()