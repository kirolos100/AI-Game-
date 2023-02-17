import pygame

from imports import import_folder
from level import *
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, path_list):
        super().__init__()
        self.import_character_assets()

        self.frame_index = 0 #index of animations dic
        self.animation_speed = 0.15 # animation update speed
        self.image = self.animations['run'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        #Player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.path_lis = path_list


        #player status
        self.status = 'run'
        self.dir = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.jump_flag = False


    #Animations
    def import_character_assets(self):
        character_path = '../graphics/enemy/'
        self.animations = {'run': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    # def import_run_particles(self):
    #     self.dust_run_particles = import_folder('../graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        #loop over the frames
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0

        if(self.dir):
            self.image = pygame.transform.flip(animation[int(self.frame_index)], True, False)

        else:
            self.image = animation[int(self.frame_index)]




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





    #Movement
    def movement(self, movement_list):
        keys = pygame.key.get_pressed()

        x_increasing = False
        x_decreasing = False
        y_increasing = False
        y_decreasing = False

        old_moves = movement_list[0]
        for moves in movement_list:
            #x tzed w t2el, el y sabta
            if old_moves[0] < moves[0] and old_moves[1] == moves[1]:
                x_increasing = True
                old_moves = moves

            elif old_moves[0] > moves[0] and old_moves[1] == moves[1]:
                x_decreasing= True
                old_moves = moves

            #X sabta, y tzed w t2el

            elif old_moves[0] == moves[0] and old_moves[1] < moves[1]:
                y_increasing = True
                old_moves = moves

            elif old_moves[0] == moves[0] and old_moves[1] > moves[1]:
                y_decreasing = True
                old_moves = moves

            #x tzed, y tzed . x t2el, y t2el

            elif old_moves[0] < moves[0] and old_moves[1] < moves[1]:
                y_increasing = True
                x_increasing = True

            elif old_moves[0] > moves[0] and old_moves[1] > moves[1]:
                y_decreasing = True
                x_decreasing = True

            #x tzed, y t2el. x t2el y tzed

            elif old_moves[0] < moves[0] and old_moves[1] > moves[1]:
                x_increasing = True
                y_decreasing = True

            elif old_moves[0] > moves[0] and old_moves[1] < moves[1]:
                x_decreasing = True
                y_increasing = True

        if self.on_ground and y_increasing:
            # self.jump()
            self.jump_flag = True
            if self.on_right or self.on_left:
                self.jump()
            self.dir = True
            self.direction.x = 1
            self.on_left = False

        if self.on_ground and y_decreasing:

            self.dir = False
            self.jump_flag = False
            if self.on_left or self.on_right:
                self.jump()
            self.direction.x = -1
            self.on_right = False

        if self.jump_flag:
            self.direction.x = 1
        else:
            self.direction.x = -1




    #GRAVITY
    def gravity_app(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    #jump
    def jump(self):
        self.direction.y = self.jump_speed



    def update(self):

        self.movement(self.path_lis)
        self.animate()