# shop.py
# mechanics für den Shop zwischen den Leveln
import pygame

class Shop:

    def shop_start (self):
        #ersetllen einer liste in dem die items gespeichert werden
        self.shop_items = []

        # einzelne items in shop erstelen mit eigenen werten
        self.shop_items.append ({
           "rect": pygame.Rect (80, 300 , 120, 120),
           "name": "Damage Up",
           "price": 50,
           "effect": "damage"
        })
        self.shop_items.append ({
           "rect": pygame.Rect (240, 300 , 120, 120),
           "name": "Fire Rate Up",
           "price": 50,
           "effect": "fire_rate"
           })
        self.shop_items.append ({
           "rect": pygame.Rect (400, 300 , 120, 120),
           "name": "Shot Speed Up",
           "price": 50,
           "effect": "shot_speed"
           })
        self.shop_items.append ({
           "rect": pygame.Rect (100, 450 , 400, 120),
           "name": "Heal full",
           "price": 20,
           "effect": "healing"
           })
       
        

    
    def handle_click(self, mouse_pos, player, points):
        # Funktion damit nur einmal etwas gekauft wird pro click
        for item in self.shop_items:
            if item["rect"].collidepoint(mouse_pos):
                points = self.buy_upgrade(item, player, points)
                break
        return points
    
    def buy_upgrade (self, item, player, points):

        #Upgrade Mechanik

        if points < item["price"]:
            print("Nicht genügeng Points") #DEBUG
            return points
        

        if  item["effect"] == "damage":
            player.dmg += 5

        
        if  item["effect"] == "fire_rate":
            if player.cad > 6: #max fire rate
                player.cad -= 1
            else:
                print ("Max Fire Rate")
                return points
 
        if  item["effect"] == "shot_speed":
            player.shotspd += 2
   
        if  item["effect"] == "healing":
            if player.hp == 100:
                print ("Full HP")
                return points
            else:
                player.hp = 100



        points -= item["price"]
        print ("Points:",points) #DEBUG
        
        print(f"{item['name']} upgrdaded -{item['price']} points") #DEBUG
    
        return points

    def draw_shop (self, screen: pygame.Surface, SCREEN_WIDTH, SCREEN_HEIGHT, player, points):
        
        # Allgemeiner Text
        font = pygame.font.SysFont(None, 72)
        text = font.render("Level Completed!", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 350))

        font = pygame.font.SysFont(None, 50)
        text = font.render("Press SPACE to continue", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 250))

        #Score zeigem
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Current Score: {points}", True, (150, 50, 200))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 250))

        # Aktuelle Stats zeichnen
        font = pygame.font.SysFont(None, 30) # Stat Font
        #Damage
        text = font.render(f"DMG: {player.dmg}", True, (255, 255, 255))
        screen.blit(text, (80, SCREEN_HEIGHT // 2 - 200))
        #Fire Rate
        text = font.render(f"Firerate: {player.cad}", True, (255, 255, 255))
        screen.blit(text, (240, SCREEN_HEIGHT // 2 - 200))
        #Shot Speed
        text = font.render(f"Shot Speed: {player.shotspd}", True, (255, 255, 255))
        screen.blit(text, (400, SCREEN_HEIGHT // 2 - 200))
        #HP Bar
        #print (hp) #DEBUG
        font = pygame.font.SysFont(None, 50)
        text = font.render(f"HP: {player.hp}/100", True, (255, 80, 80))
        screen.blit(text, (SCREEN_WIDTH - 230 , SCREEN_HEIGHT - 70))


        #Upgrades zeichnen
        font = pygame.font.SysFont(None, 24) #Allgemeine Upgrade Font

        for item in self.shop_items:

            rect = item["rect"]

            # zeichnet boxen
            pygame.draw.rect(screen, (180, 180, 180), rect)

            #Die Namen in der Upgrade Box zentrieren
            name_text = font.render(item["name"], True, (0, 0, 0))
            name_rect = name_text.get_rect(center=(rect.centerx, rect.centery - 15))
            screen.blit(name_text, name_rect)

            #Die Preise der Items schreiben
            price_text = font.render(f"-{item['price']} points", True, (100, 0, 100))
            price_rect = price_text.get_rect(center=(rect.centerx, rect.centery + 15))
            screen.blit(price_text, price_rect)
