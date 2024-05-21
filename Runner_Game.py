import pygame 
from sys import exit
from random import randint,choice

def display_score():

    current_time = pygame.time.get_ticks()//1000 - start_time
    score_surf = game_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    score_rect_inflated = score_rect.inflate(20,10)
    pygame.draw.rect(screen,'#c0e8ec',score_rect_inflated,0,2)
    screen.blit(score_surf,score_rect)
    return current_time

def add_obstacle(obstacle_rect_list,type):
    match type:
        case 'fly': obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))
        case 'snail': obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))

def obstacle_movement(obstacle_rect_list):
    if obstacle_rect_list:
        current_time = pygame.time.get_ticks()//1000 - start_time

        for obstacle_rect in obstacle_rect_list:
            obstacle_rect.x -= (4.5 + current_time // 10)
            if obstacle_rect.bottom == 300 : screen.blit(snail_surf,obstacle_rect)
            else : screen.blit(fly_surf,obstacle_rect)

        obstacle_rect_list = [obstacle for obstacle in obstacle_rect_list if obstacle.x > -100]

        return obstacle_rect_list

    else: return[]

def collisions(player,obstacle_rect_list):
    if obstacle_rect_list:
        for obstacle_rect in obstacle_rect_list:
            obstacle_hit_box = pygame.Rect.copy(obstacle_rect)
            obstacle_hit_box = obstacle_hit_box.scale_by(0.8,0)
            player_hit_box = player.scale_by(0.75,0)
            if player_hit_box.colliderect(obstacle_hit_box): return False 
    return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock=pygame.time.Clock()
game_font = pygame.font.Font('font/Pixeltype.ttf', 50) 
game_active = False
player_gravity = 0
start_time = 0
score = 0
obstacle_rect_list = []

# Loading Images'/Fonts' surfs and rects 
background_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

 # obstacles
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('graphics/Fly/Fly1.png')

 # game screen
player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80,300))

 # intro screen
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf,0,2)
player_stand_rect = player_stand_surf.get_rect(center = (400,200))

 # text
game_name_surf = game_font.render('Space Runner',False,(111,196,169))
game_name_rect = game_name_surf.get_rect(center =(400,50))

game_message_surf = game_font.render('Press Space to Play',False,(111,196,169))
game_message_rect = game_message_surf.get_rect(center =(400,350))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,2000)


# Game Update Loop
while True:

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 280:
                    game_active = True
                    player_gravity = -20

            if event.type == obstacle_timer:
                add_obstacle(obstacle_rect_list,choice(['fly','snail','snail','snail']))

                
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() // 1000 
            
        
    if game_active:
        # Transfering Rect on Screen
        screen.blit(background_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        screen.blit(player_surf,player_rect)
        
        # Diplaying Score
        score = display_score()
        
        # Player Jump Logic
        player_gravity += 0.97
        player_rect.y += player_gravity

        # Player Grounding 
        if player_rect.bottom >= 300 : player_rect.bottom = 300

        # Obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collisions
        game_active = collisions(player_rect,obstacle_rect_list)


    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity=0

        screen.fill((94,129,162))
        screen.blit(player_stand_surf,player_stand_rect)
        screen.blit(game_name_surf,game_name_rect)
        score_message_surf = game_font.render(f'Your Score: {score}',False,(111,196,169))
        score_message_rect = score_message_surf.get_rect(center =(400,350))
        if score == 0:
            screen.blit(game_message_surf,game_message_rect)
        else:
            screen.blit(score_message_surf,score_message_rect)

    pygame.display.update()
    # Setting Max FPS
    clock.tick(60)