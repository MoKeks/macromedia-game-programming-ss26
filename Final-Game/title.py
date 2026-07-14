# gameover.py
#gameover functions
import pygame

class Title:
    def draw_title (self, screen: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT):
        
    
        #Title Text
        font = pygame.font.SysFont(None, 72)
        text = font.render("Real Game!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

        font = pygame.font.SysFont(None, 16)
        text = font.render("Trust Me :3", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 150))


        font = pygame.font.SysFont(None, 60)
        text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))
            
          