import pygame
import os

# Change Directory # Random Error 01
os.chdir(os.path.dirname(os.path.abspath(__file__)))

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 480
run = True    
FPS = 60
game_status = 'Running'
is_pause = False
pause_delay_count = 0

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Goblin")
clock = pygame.time.Clock()

# Bullet
bullet_width = bullet_height = 16
bullet_list = []
FIRE_DELAY = 30
fire_delay_count =0
is_shot = False

# Player
player_width = 64
player_height = 64
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = (SCREEN_HEIGHT - player_height)
player_velocity = 2

# Enemy
enemy_list = []
enemy_spawn_x = 5
enemy_spawn_y = SCREEN_HEIGHT - 58
enemy_velocity = 2

# Sprite
Walk_Right = []
Walk_Left = []
Enemy_Right = []
Enemy_Left = []

tower_img = pygame.image.load(os.path.join('Sprite', 'tower.png'))
tower_img = pygame.transform.smoothscale(tower_img, (100, 100))

goblin_img = pygame.image.load(os.path.join('Sprite', 'goblin.png'))
goblin_img = pygame.transform.smoothscale(goblin_img, (44, 44))

bullet_right = pygame.image.load(os.path.join('Sprite', "bullet.png")).convert_alpha()
bullet_right = pygame.transform.smoothscale(bullet_right, (bullet_width, bullet_height))

bullet_left = pygame.transform.flip(bullet_right, True, False)

bg = pygame.image.load(os.path.join('Sprite', 'bg.jpg'))
char = pygame.image.load(os.path.join('Sprite', 'standing.png'))

for i in range(1, 10):
    Walk_Right.append(pygame.image.load(os.path.join('Sprite', f'R{i}.png')))
    Walk_Left.append(pygame.image.load(os.path.join('Sprite', f'L{i}.png')))   
    Enemy_Right.append(pygame.image.load(os.path.join('Sprite', f'R{i}E.png')))
    Enemy_Left.append(pygame.image.load(os.path.join('Sprite', f'L{i}E.png')))   

# Person
class Person():
    def __init__(self,x,y,width,height,velocity,):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.is_right = False
        self.is_left = False
        self.is_standing_still = True
        self.walk_count = 0
        self.is_jump = False
        self.jump_down = False
        self.jump_count = 10
        self.hitbox_width = self.width-30
        self.hitbox_height = self.height-7
        self.score = 0

    def add_walkcount(self):
        if self.walk_count < 30:
            self.walk_count += 1

        else:
            self.walk_count = 1

    def walk_right(self):
        self.x += man.velocity
        self.is_right = True
        self.is_left = False
        self.is_standing_still = False
        self.add_walkcount()

    def walk_left(self):
        self.x -= self.velocity
        self.is_right = False
        self.is_standing_still = False
        self.is_left = True
        self.add_walkcount()
            
    def jump(self):
        if self.jump_count > 0:
            self.y -= (self.jump_count**2) / 7
            self.jump_count = round(self.jump_count - 0.3, 2)
        
        elif self.jump_down:
                if self.jump_count < -0.1:                
                    self.y += (self.jump_count**2) / 7 
                    self.jump_count = round(self.jump_count + 0.3, 2)                  

                else:
                    self.jump_down = False
                    self.is_jump = False
                    self.jump_count = 10.0

        else:
            self.jump_count = -10.0
            self.jump_down = True

    def check_collision(self, enemy_hitbox_data, ): # 2 Axis - 1D method # Enemy X Player
        global game_status
        enemy_x, enemy_y, enemy_hit_width, enemy_hit_heigh, _, _ = enemy_hitbox_data
        
        if (enemy_x > self.hitbox_x and enemy_x < self.hitbox_x + self.hitbox_width) or (enemy_x + enemy_hit_width > self.hitbox_x and enemy_x + enemy_hit_width < self.hitbox_x + self.hitbox_width):
            if ((enemy_y > self.hitbox_y and enemy_y < self.hitbox_y + self.hitbox_height) or (enemy_y + enemy_hit_heigh > self.hitbox_y and enemy_y + enemy_hit_heigh < self.hitbox_y + self.hitbox_height)):
                game_status = 'Lose'


    def update(self, enemy_hitbox_data):
        if self.is_right and not self.is_standing_still:
            screen.blit(Walk_Right[int(self.walk_count//3.33)-1], (self.x, self.y))

        elif self.is_left and not self.is_standing_still:
            screen.blit(Walk_Left[int(self.walk_count//3.33)-1], (self.x, self.y))

        else:
            if self.is_right:
                screen.blit(Walk_Right[0], (self.x, self.y))

            else:
                screen.blit(Walk_Left[0], (self.x, self.y))       

        self.hitbox_x = self.x+15
        self.hitbox_y = self.y+10
        
        #pygame.draw.rect(screen, 'black', (self.hitbox_x, self.hitbox_y, self.hitbox_width, self.hitbox_height),2)     
        self.check_collision(enemy_hitbox_data)

#Bullet
class Bullet():
    def __init__(self, x, y, velocity, is_player_right):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.is_player_right = is_player_right

    def check_collision(self, enemy_hitbox_data, bullet_instance, enemy_instance): # 2 Axis - 1D method
        enemy_x, enemy_y, enemy_hit_width, enemy_hit_heigh, goblin_x, goblin_y = enemy_hitbox_data
        # Bullet x Enemy
        if (enemy_x > self.x and enemy_x < self.x + bullet_width) or (enemy_x + enemy_hit_width > self.x and enemy_x + enemy_hit_width < self.x + bullet_width):
            if not (enemy_y > self.y and enemy_y > self.y + bullet_height) and not(enemy_y + enemy_hit_heigh < self.y and enemy_y + enemy_hit_heigh < self.y + bullet_height):
                bullet_list.remove(bullet_instance)
                enemy_instance.health -= 20

        # Bullet x Goblin
        if (goblin_x > self.x and goblin_x < self.x + bullet_width) or (goblin_x + enemy_hit_width > self.x and goblin_x + enemy_hit_width < self.x + bullet_width):
            if not (goblin_y > self.y and goblin_y > self.y + bullet_height) and not(goblin_y + enemy_hit_heigh < self.y and goblin_y + enemy_hit_heigh < self.y + bullet_height):
                bullet_list.remove(bullet_instance)
                enemy_instance.velocity += 0.2
                Enemy.goblin_health -= 10
                Enemy(5, SCREEN_HEIGHT - 58, 2)

    def update(self, enemy_hitbox_data, bullet_instance, enemy_instance):
        if self.is_player_right:
            screen.blit(bullet_right, (self.x, self.y)) # Right Side Perfect

        else:
            screen.blit(bullet_left, (self.x, self.y)) # Right Side Perfect

        #pygame.draw.rect(screen, 'black', (self.x, self.y, bullet_width, bullet_height), 2)
        self.check_collision(enemy_hitbox_data, bullet_instance, enemy_instance)

# Enemy
class Enemy():
    goblin_y = 320
    goblin_x = 5
    goblin_health = 100
    is_goblin_up = True

    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.is_right = True
        self.walk_count = 0
        self.attacked = 0
        self.health = 100

    def get_hitbox_data(self):
        if self.is_right:
            return (self.x+15, self.y+5, 64-40, 64-15, Enemy.goblin_x, Enemy.goblin_y)
        
        else:
            return (self.x+30, self.y+5, 64-40, 64-5, Enemy.goblin_x, Enemy.goblin_y)
        
    def update(self, man_instance):
        if not (self.health <= 0):
            if not (self.x < (SCREEN_WIDTH - 64) - self.velocity):
                self.is_right = False

            elif not (self.x > self.velocity):
                self.is_right = True

            if self.is_right:
                self.x += self.velocity
            
            else:
                self.x -= self.velocity

            # Walk Count
            if self.walk_count <= 60:
                self.walk_count += 1

            else:
                self.walk_count = 0

            # Draw
            if self.is_right:
                screen.blit(Enemy_Right[int(self.walk_count//6.66)-1], (self.x, self.y))
                #pygame.draw.rect(screen, 'black', (self.x+15, self.y+5, 64-40, 64-15),2)

            else:
                screen.blit(Enemy_Left[int(self.walk_count//6.66)-1], (self.x, self.y))
                #pygame.draw.rect(screen, 'black', (self.x+30, self.y+5, 64-40, 64-5),2)

            pygame.draw.rect(screen, 'red', (self.x, self.y - 10, 50, 10))
            pygame.draw.rect(screen, (3,53,0), (self.x, self.y - 10, self.health//2, 10))
            pygame.draw.rect(screen, 'black', (self.x, self.y - 10, 50, 10), 2)        


        else:
            self.x = 5
            self.y = SCREEN_HEIGHT - 58
            self.is_right = True
            man_instance.score += 5  
            self.walk_count = 0
            self.attacked = 0
            self.health = 100
            self.velocity += 0.1
    
    @staticmethod
    def float_goblin(man_instance):
        global game_status

        if Enemy.is_goblin_up:
            if Enemy.goblin_y > 310:
                Enemy.goblin_y -= 0.4

            else:
                Enemy.is_goblin_up = False

        else:
            if Enemy.goblin_y < 330:
                Enemy.goblin_y += 0.4

            else:
                Enemy.is_goblin_up = True    

        screen.blit(goblin_img, (Enemy.goblin_x,Enemy.goblin_y))
        pygame.draw.rect(screen, 'red', (Enemy.goblin_x, 330 - 44, 50, 10))
        pygame.draw.rect(screen, (3,53,0), (Enemy.goblin_x, 330 - 44, Enemy.goblin_health//2, 10))
        #pygame.draw.rect(screen, 'black', (Enemy.goblin_x, 330 - 44, 50, 10), 2)

        if Enemy.goblin_health <= 0:
            game_status = 'Won'
            man_instance.score += 20


def reset():
    global bullet_list, fire_delay_count, is_shot, game_status, man, enemy
    
    game_status = "Running"
    bullet_list = []
    fire_delay_count = 0
    is_shot = False
    man = Person(player_x,player_y,player_width,player_height,player_velocity)
    enemy = Enemy(5, SCREEN_HEIGHT - 58, 2)
    Enemy.goblin_health = 100

def pause():
    global is_pause, pause_delay_count

    screen.blit(bg,(0,0)) 
    text = font_2.render(f'Game Paused', True, 'black') 
    screen.blit(text, (SCREEN_WIDTH//2-120, SCREEN_HEIGHT//2-20))
    text = font_1.render('Press Esc To Unpause', True, 'black') 
    screen.blit(text, (SCREEN_WIDTH//2-110, SCREEN_HEIGHT//2+20))

    if keys[pygame.K_ESCAPE] and pause_delay_count > 20:
        is_pause = False

    else:
        pause_delay_count += 1        

# Main Character
man = Person(player_x,player_y,player_width,player_height,player_velocity)
enemy = Enemy(5, SCREEN_HEIGHT - 58, 2) # One Enemy at the start
font_1 = pygame.font.SysFont('LCD', 30)
font_2 = pygame.font.SysFont('Unispace', 60)

def refresh_screen():
    global game_status, bullet_list, fire_delay_count, is_shot, game_status, man, enemy, pause_delay_count

    if game_status == 'Running' and not is_pause:
        pause_delay_count = 0
        pygame.draw.rect(screen, 'brown', (0,470,SCREEN_WIDTH,10))
        
        # Goblin
        screen.blit(tower_img, (-23,375))
        Enemy.float_goblin(man)
        man.update(enemy.get_hitbox_data())
        enemy.update(man)
        
        # Score Display
        score_disp = font_1.render(f'Score: {man.score}', True, 'black') 
        screen.blit(score_disp, (SCREEN_WIDTH-130, 5))      

    elif game_status == 'Won':
        screen.blit(bg,(0,0,)) 
        text = font_2.render(f'You Win!', True, 'black') 
        screen.blit(text, ((SCREEN_WIDTH//2)-70, (SCREEN_HEIGHT//2)-50))   
        text = font_1.render(f'Score: {man.score}', True, 'black') 
        screen.blit(text, (SCREEN_WIDTH//2-25, SCREEN_HEIGHT//2))
        text = font_1.render('Press Enter To Restart', True, 'black') 
        screen.blit(text, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+40))

        if keys[pygame.K_RETURN]:
            reset()

    elif game_status == 'Lose':
        screen.blit(bg, (0,0)) 
        text = font_2.render(f'You Lose!', True, 'black') 
        screen.blit(text, ((SCREEN_WIDTH//2)-70, (SCREEN_HEIGHT//2)-50))  
        text = font_1.render(f'Score: {man.score}', True, 'black') 
        screen.blit(text, (SCREEN_WIDTH//2-25, SCREEN_HEIGHT//2))  
        text = font_1.render('Press Enter To Restart', True, 'black') 
        screen.blit(text, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+40))

        if keys[pygame.K_RETURN]:
            reset()

    if is_pause:
        pause()

    pygame.display.update()
    clock.tick(FPS)

while run:
    screen.blit(bg, (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #Bullet
    for bullet in bullet_list:
        if bullet.x > SCREEN_WIDTH or bullet.x < 0:
            bullet_list.remove(bullet)
            
        if bullet.is_player_right:
            bullet.x += bullet.velocity

        else:
            bullet.x -= bullet.velocity

        bullet.update(enemy.get_hitbox_data(), bullet, enemy)

    # Key
    keys = pygame.key.get_pressed()
    
    if game_status == 'Running':
        # Pause
        if keys[pygame.K_ESCAPE]:
            is_pause = True

        # Walk
        if keys[pygame.K_LEFT] and man.x > man.velocity: # LEFT
            man.walk_left()
                
        elif keys[pygame.K_RIGHT] and man.x < (SCREEN_WIDTH - man.width) - man.velocity: # RIGHT
            man.walk_right()     

        else: # Standing Still
            man.is_standing_still = True     

        # Shoot Bullet
        if not is_shot:
            if keys[pygame.K_f]:
                if len(bullet_list) < 5:
                    bullet_list.append(Bullet((man.x + man.width//2) - 7, man.y + player_height//2, 7, man.is_right))
                    is_shot = True
        
        else:
            if fire_delay_count < FIRE_DELAY:
                fire_delay_count += 1
            
            else:
                fire_delay_count = 0
                is_shot = False

        # JUMP
        if not (man.is_jump):
            if keys[pygame.K_SPACE] and man.x > (100-23): # JUMP
                man.is_jump = True

        else: # JUMP
            man.jump()

    # Refresh, ReDraw
    refresh_screen()

pygame.quit() 