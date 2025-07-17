import pygame, sys, random, os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Window settings
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

# Load dino animation frames
dino_img1 = pygame.transform.scale(pygame.image.load("assets/dino_1.png"), (60, 60))
dino_img2 = pygame.transform.scale(pygame.image.load("assets/dino_2.png"), (60, 60))

# Load cactus variants
cactus_imgs = [
    pygame.transform.scale(pygame.image.load("assets/cactus.png"), (40, 60)),
    pygame.transform.scale(pygame.image.load("assets/cactus_tall.png"), (60, 80)),
    pygame.transform.scale(pygame.image.load("assets/cactus_small.png"), (30, 40))
]

# Ground and backgrounds
ground_img = pygame.transform.scale(pygame.image.load("assets/ground.png"), (WIDTH, 60))
bg_day_img = pygame.transform.scale(pygame.image.load("assets/bg.png"), (WIDTH, HEIGHT))
bg_night_img = pygame.transform.scale(pygame.image.load("assets/bg_night.png"), (WIDTH, HEIGHT))

# Load sounds
jump_sound = pygame.mixer.Sound("assets/jump.mp3")
gameover_sound = pygame.mixer.Sound("assets/gameover.mp3")
milestone_sound = pygame.mixer.Sound("assets/milestone.mp3") 

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# High Score File
HIGHSCORE_FILE = "highscore.txt"
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

class Background:
    def __init__(self):
        self.img_day = bg_day_img.convert()
        self.img_night = bg_night_img.convert()
        self.x1 = 0
        self.x2 = WIDTH
        self.y = 0
        self.speed = 1
        self.switch_timer = 0
        self.switch_interval = 1000
        self.fade_duration = 120
        self.fading = False
        self.fade_progress = 0
        self.use_day = True

    def update(self):
        self.switch_timer += 1
        if self.switch_timer >= self.switch_interval and not self.fading:
            self.fading = True
            self.fade_progress = 0
            self.switch_timer = 0
        if self.fading:
            self.fade_progress += 1
            if self.fade_progress >= self.fade_duration:
                self.fading = False
                self.use_day = not self.use_day
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 <= -WIDTH:
            self.x1 = self.x2 + WIDTH
        if self.x2 <= -WIDTH:
            self.x2 = self.x1 + WIDTH

    def draw(self):
        base_img = self.img_day if self.use_day else self.img_night
        next_img = self.img_night if self.use_day else self.img_day
        screen.blit(base_img, (self.x1, self.y))
        screen.blit(base_img, (self.x2, self.y))
        if self.fading:
            alpha = int((self.fade_progress / self.fade_duration) * 255)
            next_img_fade = next_img.copy()
            next_img_fade.set_alpha(alpha)
            screen.blit(next_img_fade, (self.x1, self.y))
            screen.blit(next_img_fade, (self.x2, self.y))

class Dino:
    def __init__(self):
        self.images = [dino_img1, dino_img2]
        self.image_index = 0
        self.image = self.images[0]
        self.x = 50
        self.y = HEIGHT - 90
        self.jump = False
        self.jump_speed = 15
        self.gravity = 0.9
        self.vel_y = 0
        self.anim_timer = 0
        self.anim_speed = 8
        self.shield = False
        self.shield_timer = 0

    def update(self):
        if self.jump:
            self.vel_y -= self.gravity
            self.y -= self.vel_y
            if self.y >= HEIGHT - 90:
                self.y = HEIGHT - 90
                self.jump = False
                self.vel_y = 0
        else:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        if self.shield:
            pygame.draw.circle(screen, (0, 150, 255), (self.x + 30, self.y + 30), 35, 2)

class Cactus:
    def __init__(self):
        self.image = random.choice(cactus_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = HEIGHT - self.rect.height - 30
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def collide(self, dino):
        dino_rect = pygame.Rect(dino.x, dino.y, 30, 60)
        return dino_rect.colliderect(self.rect)

class Ground:
    def __init__(self):
        self.x1 = 0
        self.x2 = WIDTH
        self.y = HEIGHT - 30
        self.speed = 5

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 < -WIDTH:
            self.x1 = self.x2 + WIDTH
        if self.x2 < -WIDTH:
            self.x2 = self.x1 + WIDTH

    def draw(self):
        screen.blit(ground_img, (self.x1, self.y))
        screen.blit(ground_img, (self.x2, self.y))

def game():
    global high_score
    background = Background()
    dino = Dino()
    ground = Ground()
    cacti = []
    score = 0
    milestone_played = False  # NEW
    font = pygame.font.SysFont(None, 36)

    while True:
        background.update()
        background.draw()
        ground.update()
        ground.draw()
        dino.draw()
        press_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        screen.blit(press_text, (WIDTH // 2 - 140, HEIGHT // 2))
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump_sound.play()
            break

    running = True
    while running:
        background.update()
        background.draw()
        ground.update()
        ground.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and not dino.jump:
            dino.jump = True
            dino.vel_y = dino.jump_speed
            jump_sound.play()

        if keys[pygame.K_s]:
            dino.shield = True
            dino.shield_timer = 300

        dino.update()
        dino.draw()

        if not cacti or cacti[-1].rect.x < WIDTH - random.randint(300, 500):
            if random.randint(1, 100) < 2:
                cacti.append(Cactus())

        for cactus in list(cacti):
            cactus.update()
            cactus.draw()
            if cactus.collide(dino):
                if dino.shield:
                    cacti.remove(cactus)
                    dino.shield = False
                else:
                    gameover_sound.play()
                    save_high_score(high_score)
                    show_game_over_screen(score, font)
                    return
            if cactus.rect.x < -40:
                cacti.remove(cactus)

        score += 1

        # NEW: Play milestone sound at 500
        if score >= 500 and not milestone_played:
            milestone_sound.play()
            milestone_played = True

        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        if score > high_score:
            high_score = score
        high_score_text = font.render(f"High Score: {high_score}", True, (100, 100, 100))
        screen.blit(high_score_text, (10, 40))

        pygame.display.update()
        clock.tick(FPS)

def show_game_over_screen(score, font):
    screen.fill((255, 255, 255))
    text1 = font.render("GAME OVER", True, (255, 0, 0))
    text2 = font.render(f"Score: {score}", True, (0, 0, 0))
    text3 = font.render("Press R to Restart", True, (100, 100, 100))
    screen.blit(text1, (WIDTH // 2 - 80, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - 60, HEIGHT // 2))
    screen.blit(text3, (WIDTH // 2 - 100, HEIGHT // 2 + 40))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            waiting = False

if __name__ == "__main__":
    while True:
        game()
