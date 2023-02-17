import pygame
from imports import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.import_run_particles()
        self.frame_index = 0 #index of animations dic
        self.animation_speed = 0.15 # animation update speed
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)


        #Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        #player status
        self.status = 'idle'
        self.dir = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        #Dust particles
        self.import_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface


    #Animations
    def import_character_assets(self):
        character_path = '../graphics/character/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_run_particles(self):
        self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frames
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0

        if(self.dir):
            self.image = animation[int(self.frame_index)]
        else:
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)

        #Rectangle fix
        # if self.on_ground and self.on_right:
        #     self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        #     self.direction.x = 0
        # elif self.on_ground and self.on_left:
        #     self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        #     self.direction.x = 0
        # elif self.on_ground:
        #     self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # elif self.on_ceiling and self.on_right:
        #     self.direction.x = 0
        #     self.rect = self.image.get_rect(topright = self.rect.topright)
        # elif self.on_ceiling and self.on_left:
        #     self.direction.x = 0
        #     self.rect = self.image.get_rect(topleft = self.rect.topleft)
        # elif self.on_ceiling:
        #     self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particles = self.dust_run_particles[int(self.dust_frame_index)]

            #player moving to the right
            if self.dir:
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particles, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.display_surface.blit((pygame.transform.flip(dust_particles,True,False)), pos)

    def get_stat(self):
        if self.direction.y < 0: #Upward movement:
            self.status = 'jump'
        elif self.direction.y > 1: #downward move
            self.status = 'fall'

        elif self.direction.x < 0 or self.direction.x > 0:
            self.status = 'run'
        else:
            self.status = 'idle'



    #Movement
    def movement(self):
        keys = pygame.key.get_pressed()
        if(self.direction.x > 0):
            self.dir = True
        elif(self.direction.x < 0):
            self.dir = False
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.dir = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.dir = False
        #idle
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    #GRAVITY
    def gravity_app(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    #jump
    def jump(self):
        self.direction.y = self.jump_speed



    def update(self):
        self.movement()
        self.get_stat()
        self.animate()
        self.run_dust_animation()
