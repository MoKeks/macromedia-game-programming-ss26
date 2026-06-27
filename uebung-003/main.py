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
    player.set_might(rng=10000, dmg=1, cad=0, shotspd= 1)

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

    level = Level()
    level.load("lvl001.rfg")

    game_state = Game()
    game_state.change_state("playing")


    
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

        # -------------------------------------------------------------- #
        #  Update                                                        #
        # -------------------------------------------------------------- #
          # checking for game-state
        if game_state.state == "playing":
            player.step()
            level.step()

       


        #----------------------------------------------------------------#
        # Check collisions
        #----------------------------------------------------------------#

        # Obstacle collsion
            for obstacle in level.obstacles:
                 if obstacle.collsion(player.get_rect()):
                    player.hp -= 1
                
          
        # Enemy collsion
            for enemies in level.enemies:
                if not enemies.alive :
                    continue

                if enemies.collision(player.get_rect()):
                    player.hp -= 1
                    enemies.hp -= 5
                    enemies.is_alive()

                elif enemies.collision(shot.get_rect()):
                    enemies.hp -= 1
                    enemies.is_alive()

        # Shot Collision

       
        # Check player.hp <= 0 for death / game_state transition
            if player.hp <= 0:
                game_state.change_state("gameover")

        ## game over mechanic
        elif game_state.state == "gameover":
           # wäre funny: pygame.quit # einfach spiel schließen wenn man stirbt
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over!", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()
            continue   # Spiellogik überspringen

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

        # TODO: Draw player HP (text or health bar)

        pygame.display.flip()
        clock.tick(FPS)

    # ------------------------------------------------------------------ #
    #  Cleanup                                                           #
    # ------------------------------------------------------------------ #
    pygame.quit()


if __name__ == "__main__":
    main()