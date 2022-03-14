import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.player_index=0
        self.player_gravity=0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity=0
        self.jump_scound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_scound.set_volume(0.5)
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=300:
            self.gravity = -20
            self.jump_scound.play()
        
    def apply_gravity(self):
        self.gravity +=1
        self.rect.y += self.gravity
        if self.rect.bottom >=300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else : 
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index=0
            self.image = self.player_walk[int(self.player_index)]
    
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame2 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_frame1 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            y_pos =300
            self.frames = [snail_frame1,snail_frame2]
        
        self.animation_index = 0 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))
    
    def obstacle_animation(self):
        self.animation_index +=0.1
        if self.animation_index >= len(self.frames): self.animation_index=0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.obstacle_animation()
        self.rect.x -=6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def dispkay_score():
    current_time = int(pygame.time.get_ticks()/1000)-start_time
    score_surf = test_font.render(f'{current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center=(400,60))
    screen.blit(score_surf,score_rect)
    print(current_time)
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:return True


pygame.init()

latest_score=0
screen = pygame.display.set_mode((800,400))
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()
pygame.display.set_caption('Jump Arcade')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
game_active = False
intro_text_surf = test_font.render('Pygame Jump Arcade', False, 'Black')
intro_text_rect = intro_text_surf.get_rect(center = (400,60))
start_time =0
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png')
player_stand_surf_scaled = pygame.transform.scale2x(player_stand_surf)
player_stand_surf_scaled_rect = player_stand_surf_scaled.get_rect(center = (400,200))

obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == obstacle_timer and game_active:
            obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
            print('test')
           
    #draw all our elements
    #update everyting
    if game_active:
        screen.blit(sky_surface,(0,0)) #displaying our test surface onto our main display
        screen.blit(ground_surface,(0,300))
        dispkay_score()
        bg_music.play()
       
        player.draw(screen)
        obstacle_group.draw(screen)
        obstacle_group.update()

        player.update()
       
        mouse_pos = pygame.mouse.get_pos()
        mouse_butt = pygame.mouse.get_pressed()
       
    #collision
        
     
        if not collision_sprite():
             game_active = False
             current_time = int(pygame.time.get_ticks()/1000)-start_time
             start_time = current_time
             latest_score = start_time
    else:
        screen.fill((94,129,162))
        screen.blit(intro_text_surf,intro_text_rect)
        screen.blit(player_stand_surf_scaled,player_stand_surf_scaled_rect)
        keys = pygame.key.get_pressed()
        current_score_surf = test_font.render(f'current score :{latest_score}',False,'Black')
        blink = 'Black' if int(pygame.time.get_ticks()/1000)%2==0 else 'White'
        blink_text = test_font.render('Press enter to play!',False,blink)
        current_score_rect = current_score_surf.get_rect(center= (400,380))
        blink_text_rect = blink_text.get_rect(center=(400,320))
        screen.blit(current_score_surf,current_score_rect)
        screen.blit(blink_text,blink_text_rect)
        if keys[pygame.K_RETURN]:
            latest_score=0
            game_active = True
            start_time = int(pygame.time.get_ticks()/1000)
          
    pygame.display.update()
    clock.tick(60)