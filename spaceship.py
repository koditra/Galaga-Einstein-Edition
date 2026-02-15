import pygame

class spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load("assets/graphics/spaceship.png").convert_alpha()
        self.image = pygame.transform.scale(original_image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.pos_x = float(x)

        # Sideways movement
        self.side_speed = 0
        self.side_accel = 0.8
        self.side_friction = 0.85
        self.max_side_speed = 10

        # 🚀 Forward speed (THIS is relativity speed)
        self.forward_speed = 2
        self.forward_accel = 0.05
        self.max_forward_speed = 12

    def update(self):
        keys = pygame.key.get_pressed()

        # Sideways controls
        if keys[pygame.K_LEFT]:
            self.side_speed -= self.side_accel
        if keys[pygame.K_RIGHT]:
            self.side_speed += self.side_accel

        self.side_speed *= self.side_friction
        self.side_speed = max(-self.max_side_speed, min(self.max_side_speed, self.side_speed))

        self.pos_x += self.side_speed
        self.pos_x = max(0, min(750 - self.rect.width, self.pos_x))
        self.rect.x = int(self.pos_x)

        # 🚀 Forward acceleration (hold UP)
        if keys[pygame.K_UP]:
            self.forward_speed += self.forward_accel
        else:
            # Ease back to default speed
            self.forward_speed += (2 - self.forward_speed) * 0.08
        self.forward_speed = max(2, min(self.forward_speed, self.max_forward_speed))
