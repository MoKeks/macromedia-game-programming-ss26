# main.py
# Game loop for RealFakeGame.
#
# Controls:
#   Mouse X  — move player left/right
#   ESC      — quit
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

from time import sleep

LEVEL_FILES = ["lvl001.rfg", "lvl002.rfg", "lvl003.rfg"]
#                  Index 0        1             2         


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
    player.set_might(rng= 500, dmg=1, cad=20, shotspd= 10)
    

    enemies = Enemy ()
    enemies.setup(
        x=SCREEN_WIDTH // 2,
        y=SCREEN_HEIGHT,
        dx=0,
        dy=0,
        image_prefix="enemy",
        anim_speed=1,
        hp=10,
        damage=1
    )

    boss = Boss ()

    current_level = 0
    level = Level()
    level.load(LEVEL_FILES[current_level])
    

    duration = 0

    game_state = Game()
    game_state.change_state("playing")

    points = 0
    highscore = 0
    old_highscore = highscore

    buff_duration = 0
    
    obstacle = Obstacle ()

    shot = Shot ()


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
                        elif game_state.state == "Shop":
                            current_level, level = next_level(current_level, level)
                            duration = 0                 
                           
                
                
                     
                    

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
         # NOTE: Der typo ist wichtig (apparently)
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
                    player.hp -= 5
                    enemies.hp -= 10
                    enemies.is_alive()
                    points +=  50

                for shot in player.shots :
                    if enemies.collision(shot.get_rect()):
                        enemies.hp -= 10
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
            if buff_duration > 0 :
                buff_duration -= 1
                if buff_duration == 0:
                    player.buff (False)
                    print ("buff end")
                
            # Level Duration Check
            print (duration)
            print (level.duration)
            if level.duration == duration:
                spawn_Boss (current_level, level)
            if level.duration + 10 < duration:
                if boss.hp == 0:
                    game_state.change_state("shop")
                    
                
            # if current_level > 3:
            #     if points > highscore : #highscore checken
            #         old_highscore = highscore
            #         highscore = points
            #     game_state.change_state("gameover")

                # game_state transition to game over
            if player.hp <= 0 or current_level >= 3 :
               
                if points > highscore : #highscore checken
                    old_highscore = highscore
                    highscore = points
                game_state.change_state("gameover")

        ##########################################################
        ## game over mechanic
        ###########################################################

        elif game_state.state == "gameover":
           # wäre funny: pygame.quit # einfach spiel schließen wenn man stirbt
            screen.fill(BLACK)
            
            #Victory Check
            if current_level >= 3:
                font = pygame.font.SysFont(None, 72)
                text = font.render("Victory!", True, (100, 255, 100))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

                font = pygame.font.SysFont(None, 50)
                text = font.render("Press SPACE to Restart", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
            else:
                #Game Over Text
                font = pygame.font.SysFont(None, 72)
                text = font.render("Game Over!", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))

                font = pygame.font.SysFont(None, 60)
                text = font.render("Press SPACE to Restart", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
            
            #Score und Highscore
            # Highscore abgleichen
            if points <= old_highscore:
                #Show current score
                font = pygame.font.SysFont(None, 40)
                text = font.render(f"Score: {points}", True, (150, 50, 200))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
                # bisheriger Highscore
                font = pygame.font.SysFont(None, 30)
                text = font.render(f"Highscore: {highscore}", True, (150, 50, 200))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

            else:
                #Neuer Highscore
                font = pygame.font.SysFont(None, 50)
                text = font.render(f"NEW HIGHSCORE: {points}", True, (150, 50, 200))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
                
            # print ("space") #DEBUG
           


            pygame.display.flip()
            
            

            continue   # Spiellogik überspringen

        #######################################################
        # #Shop zwischen leveln
        ##########################################################
        elif game_state.state == "shop":
            screen.fill(BLACK)


            font = pygame.font.SysFont(None, 72)
            text = font.render("Level Completed!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 350))

            font = pygame.font.SysFont(None, 50)
            text = font.render("Press SPACE to continue", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))

            #Score zeigem
            font = pygame.font.SysFont(None, 40)
            text = font.render(f"Current Score: {points}", True, (150, 50, 200))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

            pygame.display.flip()

            continue #rest nicht ausführen
            

        # -------------------------------------------------------------- #
        #  Draw                                                          #
        # -------------------------------------------------------------- #
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
    # Stats RESET
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
    damage=1
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
        hp= 50 + current_level*50,
        damage=10+ 10*current_level,
        speed = 20 + 50 * current_level,
        scale= float(3 + 2*current_level)
    )
   level.enemies.append(boss)
   return level


def next_level(current_level, level, ):
    current_level += 1

    if current_level >= len(LEVEL_FILES):
      print("Kein weiteres Level mehr")
      return current_level, level   # unverändert zurückgeben

    level = Level()
    level.load(LEVEL_FILES[current_level])
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

  
