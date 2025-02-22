import pygame
import random
import sys

# مقداردهی اولیه کتابخانه Pygame
pygame.init()

# تنظیمات بازی
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("نبرد تانک پیشرفته")

# تعریف رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
DARK_GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# تنظیمات ساعت بازی
clock = pygame.time.Clock()
FPS = 60

# تنظیمات تانک بازیکن
tank_width, tank_height = 60, 40
barrel_length = 30
player_x = WIDTH // 2 - tank_width // 2
player_y = HEIGHT // 2 - tank_height // 2
player_speed = 5

# تنظیمات گلوله‌ها
bullet_radius = 5
bullet_speed = 10
bullets = []
fire_cooldown = 0  # زمان مکث بین شلیک

# تنظیمات دشمنان
enemy_bullets = []  # لیست گلوله‌های دشمنان
enemy_cooldown = 0  # زمان مکث شلیک دشمنان
enemy_fire_chance = 0  # احتمال شلیک دشمنان
enemy_bullet_speed = 5  # سرعت گلوله‌های دشمن
enemy_level = 0  # سطح فعلی دشمنان
shooting_enemies = []  # لیست دشمنان ویژه توانا به شلیک

# تنظیمات موانع
obstacle_width, obstacle_height = 40, 40
obstacle_speed = 5  # سرعت حرکت موانع
obstacles = []  # لیست موانع

# سیستم امتیازدهی
score = 0  # امتیاز فعلی
high_score = 0  # رکورد بالاترین امتیاز
font = pygame.font.SysFont("Arial", 30, bold=True)  # فونت نمایش متن

def draw_tank(x, y):
    """
    تابع رسم تانک با موقعیت مشخص
    - بدنه اصلی
    - برجک
    - لوله توپ
    """
    pygame.draw.rect(screen, DARK_GREEN, (x, y, tank_width, tank_height))
    pygame.draw.rect(screen, DARK_GREEN, (x + tank_width//2 - 10, y - 20, 20, 20))
    pygame.draw.line(screen, DARK_GREEN, 
                    (x + tank_width//2, y - 20), 
                    (x + tank_width//2, y - 20 - barrel_length), 5)

def draw_bullet(x, y, color=YELLOW):
    """تابع رسم گلوله با رنگ پیشفرض زرد"""
    pygame.draw.circle(screen, color, (x, y), bullet_radius)

def draw_obstacle(x, y, is_shooter=False):
    """
    تابع رسم موانع
    - موانع معمولی: مستطیل قرمز
    - موانع ویژه: مثلث بنفش
    """
    if is_shooter:
        points = [
            (x + obstacle_width//2, y),
            (x, y + obstacle_height),
            (x + obstacle_width, y + obstacle_height)
        ]
        pygame.draw.polygon(screen, PURPLE, points)
    else:
        pygame.draw.rect(screen, RED, (x, y, obstacle_width, obstacle_height))

def draw_score():
    """تابع نمایش امتیاز و رکورد در صفحه"""
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    hs_text = font.render(f"Best Record: {high_score}", True, WHITE)
    screen.blit(hs_text, (WIDTH - hs_text.get_width() - 10, 10))
    
    if enemy_level > 0:
        level_text = font.render(f"Enemey Level: {enemy_level}", True, RED)
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 10))

def game_over_screen():
    """تابع نمایش صفحه پایان بازی و مدیریت انتخاب کاربر"""
    global score, high_score
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as f:
            f.write(str(high_score))
    
    over_font = pygame.font.SysFont("Arial", 64, bold=True)
    over_text = over_font.render("Game Over!", True, RED)
    score_text = font.render(f"Your Score {score}", True, GREEN)
    hs_text = font.render(f"Best Record: {high_score}", True, GREEN)
    restart_text = font.render("For Restart Game Tap Space", True, WHITE)
    quit_text = font.render("For Exit Tap Esc", True, WHITE)
    
    while True:
        screen.fill(BLACK)
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        screen.blit(hs_text, (WIDTH//2 - hs_text.get_width()//2, HEIGHT//2 + 20))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))
        screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 120))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def main():
    """تابع اصلی اجرای بازی"""
    global player_x, player_y, score, obstacle_speed, high_score
    global fire_cooldown, enemy_cooldown, enemy_fire_chance, enemy_bullet_speed, enemy_level
    
    while True:
        # بازنشانی متغیرهای بازی برای شروع مجدد
        player_x = WIDTH // 2 - tank_width // 2
        player_y = HEIGHT // 2 - tank_height // 2
        score = 0
        obstacles.clear()
        bullets.clear()
        enemy_bullets.clear()
        shooting_enemies.clear()
        obstacle_speed = 5
        enemy_fire_chance = 0
        enemy_bullet_speed = 5
        enemy_level = 0
        last_speed_increase = 0
        
        run = True
        obstacle_timer = 0
        
        while run:
            screen.fill(BLACK)
            fire_cooldown = max(0, fire_cooldown - 1)
            enemy_cooldown = max(0, enemy_cooldown - 1)
            
            # مدیریت رویدادهای بازی
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and fire_cooldown == 0:
                        bullets.append([player_x + tank_width//2, player_y - barrel_length - 20])
                        fire_cooldown = 15
            
            # کنترل حرکت تانک با کلیدهای جهت‌دار
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < WIDTH - tank_width:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < HEIGHT - tank_height:
                player_y += player_speed
            
            # سیستم شلیک دشمنان (فعال پس از 300 امتیاز)
            if score >= 300:
                enemy_level = min((score - 300) // 50 + 1, 10)
                enemy_fire_chance = min(0.005 + (enemy_level * 0.002), 0.03)
                enemy_bullet_speed = obstacle_speed + 5
                
                if enemy_cooldown == 0:
                    for obs in obstacles[:]:
                        if obs not in shooting_enemies and random.random() < 0.1:
                            shooting_enemies.append(obs)
                        
                        if obs in shooting_enemies and random.random() < enemy_fire_chance:
                            bullet_x = obs[0] + obstacle_width//2
                            bullet_y = obs[1] + obstacle_height + 10
                            enemy_bullets.append([bullet_x, bullet_y])
                            enemy_cooldown = max(5, 30 - (enemy_level * 2))
            
            # بروزرسانی موقعیت گلوله‌های دشمن
            for bullet in enemy_bullets[:]:
                bullet[1] += enemy_bullet_speed
                
                if bullet[1] > HEIGHT:
                    enemy_bullets.remove(bullet)
                    continue
                
                # بررسی برخورد با بازیکن
                bullet_rect = pygame.Rect(bullet[0]-bullet_radius, bullet[1]-bullet_radius, 
                                        bullet_radius*2, bullet_radius*2)
                tank_rect = pygame.Rect(player_x, player_y, tank_width, tank_height)
                if bullet_rect.colliderect(tank_rect):
                    run = False
            
            # ایجاد موانع جدید
            obstacle_timer += 1
            if obstacle_timer > 30:
                obstacle_x = random.randint(0, WIDTH - obstacle_width)
                obstacles.append([obstacle_x, -obstacle_height])
                obstacle_timer = 0
            
            # مدیریت گلوله‌های بازیکن
            for bullet in bullets[:]:
                bullet[1] -= bullet_speed
                if bullet[1] < 0:
                    bullets.remove(bullet)
                    continue
                
                bullet_rect = pygame.Rect(bullet[0]-bullet_radius, bullet[1]-bullet_radius, 
                                        bullet_radius*2, bullet_radius*2)
                for obs in obstacles[:]:
                    obstacle_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
                    if bullet_rect.colliderect(obstacle_rect):
                        obstacles.remove(obs)
                        bullets.remove(bullet)
                        score += 5
                        if obs in shooting_enemies:
                            shooting_enemies.remove(obs)
                        break
            
            # حرکت موانع به پایین صفحه
            for obs in obstacles[:]:
                obs[1] += obstacle_speed
                if obs[1] > HEIGHT:
                    obstacles.remove(obs)
                    if obs in shooting_enemies:
                        shooting_enemies.remove(obs)
                    score += 1
            
            # افزایش تدریجی سختی بازی
            if score - last_speed_increase >= 10:
                obstacle_speed += 0.3
                last_speed_increase = score
            
            # بررسی برخورد تانک با موانع
            tank_rect = pygame.Rect(player_x, player_y, tank_width, tank_height)
            for obs in obstacles:
                obstacle_rect = pygame.Rect(obs[0], obs[1], obstacle_width, obstacle_height)
                if tank_rect.colliderect(obstacle_rect):
                    run = False
            
            # رسم تمامی اجزای بازی
            draw_tank(player_x, player_y)
            for obs in obstacles:
                draw_obstacle(obs[0], obs[1], obs in shooting_enemies)
            for bullet in bullets:
                draw_bullet(bullet[0], bullet[1])
            for bullet in enemy_bullets:
                draw_bullet(bullet[0], bullet[1], BLUE)
            draw_score()
            
            pygame.display.flip()
            clock.tick(FPS)
        
        # نمایش صفحه پایان بازی و بررسی انتخاب کاربر
        if not game_over_screen():
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()