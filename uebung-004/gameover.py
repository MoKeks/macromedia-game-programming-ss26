# gameover.py
#gameover functions
import pygame

class Gameover:
    def draw_gameover (self, screen: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT, points, highscore, old_highscore, current_level, LEVEL_FILES):
        #Victory Check
            if current_level >= len(LEVEL_FILES):
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
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))
                # bisheriger Highscore
                font = pygame.font.SysFont(None, 30)
                text = font.render(f"Highscore: {highscore}", True, (150, 50, 200))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 150))

            else:
                #Neuer Highscore
                font = pygame.font.SysFont(None, 50)
                text = font.render(f"NEW HIGHSCORE: {points}", True, (150, 50, 200))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))