import pygame as p
from sys import exit
from random import randint,choice

class Player(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1= p.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2= p.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_jump= p.image.load("graphics/player/jump.png").convert_alpha()
        self.player_walk=[player_walk_1,player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,250))
        self.gravity = 0

    def player_input(self):
        keys = p.key.get_pressed()
        if keys[p.K_SPACE] and self.rect.bottom >=200:
            self.gravity = -20
         
        if p.mouse.get_pressed()[0] and self.rect.collidepoint(p.mouse.get_pos()):
            self.gravity = -20   
        
        
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 250:
            self.rect.bottom = 250
            
    def animation_state(self):
        if self.rect.bottom < 250:
            self.image = self.player_jump
        else:
             self.player_index += 0.1
             if self.player_index >= len(self.player_walk): self.player_index=0
             self.image = self.player_walk[int(self.player_index)]
        
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(p.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_frame_1 = p.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = p.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1,fly_frame_2]
            y_pos = 210
        
        else:
            snail_frame_1 = p.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = p.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1,snail_frame_2]
            y_pos =250
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))
    
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        
def display_score():
    current_time = p.time.get_ticks() - start_time
    score_surf = font.render(f"Score: {int((current_time/1000))}",True,'Black')
    score_rect =score_surf.get_rect(center=(400,20))
    screen.blit(score_surf,score_rect)
    
def collisons(player,obstacles):
    if p.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    return True


p.init()
screen = p.display.set_mode((800,400))
p.display.set_caption("Alien")
font = p.font.Font("Fonts/Game.otf",30)
clk = p.time.Clock()
game_active =False
start_time =0

player = p.sprite.GroupSingle()
player.add(Player())

obstacle_group = p.sprite.Group()

sky_surf = p.image.load("Sky.png").convert()
ground_surf = p.image.load("ground.png").convert()


# Start/Over Screen
player_stand = p.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = p.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center=(400,200))
top_message = font.render("Start Game",False,"Cyan")
top_message = p.transform.rotozoom(top_message,0,2.5)
top_message_rect = top_message.get_rect(center=(400,60))
bottom_message = font.render("Press The Space key To Start",False,"Cyan")
bottom_message = p.transform.rotozoom(bottom_message,0,1.5)
bottom_message_rect = bottom_message.get_rect(center=(400,320))

#timers
obstacle_timer = p.USEREVENT+1
p.time.set_timer(obstacle_timer,1500)

while True:
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
        
        if game_active:   
            if event.type == obstacle_timer:
               obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
        else:
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                game_active=True
                start_time = p.time.get_ticks()
            
    if game_active:        
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,250))
        display_score()
       
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collisons(player,obstacle_group)
        
    else:
        screen.fill((94,129,162))
        screen.blit(top_message,top_message_rect)
        screen.blit(player_stand,player_stand_rect)
        screen.blit(bottom_message,bottom_message_rect)
        player_gravity=0
        
    p.display.update()
    clk.tick(60)