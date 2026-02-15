import pygame, sys
from spaceship import spaceship
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
GREY = (20, 29, 27)
hud_bg = pygame.Surface((330, 30), pygame.SRCALPHA)
hud_bg.fill((0, 0, 0, 140))  # RGBA → last value is transparency
font = pygame.font.Font(None, 28)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Photon Blaster")
clock = pygame.time.Clock()
laser_group = pygame.sprite.Group()
fire_sound = pygame.mixer.Sound("assets/sound/fire.mp3")
spaceship = spaceship(375, 600)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)
def time_dilation(forward_speed):
    c = 12  # "speed of light"
    # Only slow time at max speed, ease into slow motion
    if forward_speed >= c:
        return 0.25
    elif forward_speed > 11.5:
        # Ease into slow motion as speed approaches c
        return 1.0 - 0.75 * (forward_speed - 11.5) / 0.5
    return 1.0
bg_before = pygame.image.load("assets/graphics/background.png").convert()
space_bg = pygame.transform.scale(bg_before, (SCREEN_WIDTH, SCREEN_HEIGHT * 2))# Start so the bottom of the image is at the bottom of the screen
bg_y = -space_bg.get_height() + SCREEN_HEIGHT
bg_speed = 4
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/graphics/missile.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (8, 24))
        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 10
    def update(self, time_scale):
        self.rect.y -= self.base_speed * time_scale
        if self.rect.bottom < 0:
            self.kill()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire bullet from center top of spaceship
                fire_sound.play()
                missile = Missile(spaceship.rect.centerx, spaceship.rect.top)
                laser_group.add(missile)
    # time_scale = time_dilation(spaceship.velocity)  # Removed: spaceship has no 'velocity' attribute
    time_scale = time_dilation(spaceship.forward_speed)
    screen.fill(GREY)
    keys = pygame.key.get_pressed()
    # Only slow background at speed of light, restore instantly when UP is released
    if spaceship.forward_speed >= 12 and keys[pygame.K_UP]:
        bg_y += spaceship.forward_speed * time_scale
    else:
        bg_y += spaceship.forward_speed
    # Draw two backgrounds for seamless vertical scrolling
    screen.blit(space_bg, (0, bg_y))
    screen.blit(space_bg, (0, bg_y - space_bg.get_height()))
    # Reset bg_y when it exceeds the background height
    if bg_y >= space_bg.get_height():
        bg_y -= space_bg.get_height()
    spaceship_group.update()
    laser_group.update(time_scale)
    # Draw game objects
    spaceship_group.draw(screen)
    laser_group.draw(screen)
    # 🟢 HUD background and text only at max speed
    if spaceship.forward_speed >= 12:
        screen.blit(hud_bg, (5, 5))
        # Glassy, transparent HUD text with shadow
        hud_string = "~SPEED OF LIGHT"
        text_color = (180, 255, 255)
        shadow_color = (0, 0, 0, 120)
        hud_text_shadow = font.render(hud_string, True, shadow_color)
        hud_text = font.render(hud_string, True, text_color)
        glass_surface = pygame.Surface((hud_text.get_width()+8, hud_text.get_height()+8), pygame.SRCALPHA)
        pygame.draw.rect(glass_surface, (255,255,255,40), glass_surface.get_rect(), border_radius=8)
        glass_surface.blit(hud_text_shadow, (5, 5))
        glass_surface.blit(hud_text, (3, 3))
        screen.blit(glass_surface, (7, 7))
    pygame.display.update()
    clock.tick(60)
