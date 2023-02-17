import pygame
from tiles import *
from settings import *
from player import Player
from enemy import Enemy
from queue import Queue


class Level:
    def __init__(self, level_data, surface):
        #level setup
        self.display_surface = surface
        self.bfs(level_data)
        self.level_setup(level_data) #Calling the level setup with the list of the map

        self.world_shift = 0
        self.current_x = 0
        self.game_status = True
        self.game_restart = True

        #Backgrounds
        self.background = pygame.image.load("../graphics/backgrounds/bluemoon.png")
        self.gameover = pygame.image.load("../graphics/backgrounds/gameover.png")

        #BFS
        self.target_pos
        self.target_x
        self.target_y

        self.start_pos
        self.start_x
        self.start_y

        self.adj_list_numero
        self.visited
        self.level
        self.parent
        self.bfs_traversal_output
        self.queue
        self.path

    def level_setup(self, layout):
        # Player
        self.player = pygame.sprite.GroupSingle()
        #Tiles
        self.tiles = pygame.sprite.Group()
        #enemy
        self.enemy = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row): #Adding to the group of sprites of tiles the tiles with its positions using level_data list
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':

                    tile = tiles((x,y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':

                    player = Player((x, y), self.display_surface) #constructor
                    self.player.add(player)
                if cell == 'E':
                    enemy = Enemy((x,y), self.display_surface, self.path)
                    self.enemy.add(enemy)

    def bfs(self, layout):
        self.adj_list = {}
        self.adj_list_numero = []
        self.visited = {}
        self.level = {}
        self.parent = {}
        self.bfs_traversal_output = []
        self.queue = Queue()
        self.path = []

        for col_index, cols in enumerate(layout):

            for row_index, cells in enumerate(cols):
                x = col_index
                y = row_index
                print(x,", ", y, "\n")
                if cells == 'X' :

                    self.adj_list_numero.append((col_index, row_index))  # append col_index
                if cells == 'P':
                    self.adj_list_numero.append((col_index, row_index))  # append col_index
                if cells == 'E':
                    self.adj_list_numero.append((col_index, row_index))  # append col_index

        for col_index, cols in enumerate(layout):
            for row_index, cells in enumerate(cols):
                x = col_index
                y = row_index
                self.adj_list[(x,y)] = []
                if cells == 'P':
                    self.target_x = x
                    self.target_y = y
                    self.target_pos = (x,y)
                if cells == 'E':
                    self.start_pos = (x,y)
                    self.start_x = x
                    self.start_y = y

                for cols in self.adj_list_numero:
                    if(cols[0]-1 <= col_index <= cols[0]+1) and (cols[1] - 1 <= row_index <= cols[1] + 1):

                        # nafs el row bas m4 nafs el col
                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] - 1 and y == cols[1]:
                            #ya ta7t ya fo2
                            if (cols[0] - 1, cols[1]) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0]-1, row_index))

                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] +1 and y == cols[1]:
                            #ya ta7t ya fo2
                            if (cols[0] + 1, cols[1]) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0]+1, row_index))

                        #nafs el col bas m4 nafs el row

                        if cells == 'X' or cells == 'P' or cells == 'E' and y == cols[1] -1 and x == cols[0]:
                            #ya ta7t ya fo2
                            if (cols[0], cols[1] - 1) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((x, cols[1] - 1))

                        if cells == 'X' or cells == 'P' or cells == 'E' and y == cols[1] +1 and x == cols[0]:
                            #ya ta7t ya fo2
                            if (cols[0], cols[1]+1) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((x, cols[1] + 1))

                        #top right top left bot right bot left

                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] -1 and y == cols[1] + 1: #Top right

                            if (cols[0] - 1, cols[1] + 1) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0] - 1, cols[1] + 1))

                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] -1 and y == cols[1] - 1: #Top left

                            if (cols[0] - 1, cols[1] - 1) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0] - 1, cols[1] - 1))

                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] +1 and y == cols[1] + 1: #bott right

                            if (cols[0] + 1, cols[1] + 1) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0]+ 1, cols[1]+ 1))

                        if cells == 'X' or cells == 'P' or cells == 'E' and x == cols[0] +1 and y == cols[1] - 1: #bott left

                            if (cols[0], cols[1]) in self.adj_list_numero:
                                self.adj_list[(x, y)].append((cols[0] + 1, cols[1] - 1))


        # BFS

        self.level = {}
        for node in self.adj_list.keys():
            self.visited[node] = False
            self.parent[node] = None
            self.level[node] = -1  # or infinity


        s = self.target_pos
        self.visited[s] = True
        self.level[s] = 0

        self.queue.put(s)

        while not self.queue.empty():
            u = self.queue.get() #Dequeue
            self.bfs_traversal_output.append(u)

            for v in self.adj_list[u]:
                if not self.visited[v]:
                    self.visited[v] = True
                    self.parent[v] = u
                    self.level[v] = self.level[u] + 1
                    self.queue.put(v)

        #Adjusting the adjancy_list
        temp = []
        res = dict()

        for key, val in self.adj_list.items():
            if val not in temp:
                temp.append(val)
                res[key] = val
        res.pop((0, 0))

        for key, val in res.items():
            for i in val:
                val = list(dict.fromkeys(val))
                res[key] = val

        self.adj_list = res


        #Shortest path based on parents

        v = self.start_pos
        while v is not None:
            self.path.append(v)
            v = self.parent[v]





    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width and direction_x < 0: #left side of the screen
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width/4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    #Horizonal collisison

    def horiz_colli(self):
        player = self.player.sprite

        #Movement changes
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():

            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:   #left collision
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                    player.direction.x = 0
                elif player.direction.x > 0: #right collision
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    player.direction.x = 0

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_colli(self):
        player = self.player.sprite

        player.gravity_app()
        for sprite in self.tiles.sprites():

            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:   #downwards collision
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground  = True
                elif player.direction.y < 0: #upwards collision
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > 1: #Player not jumping or falling
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

    def evertical_colli(self):
        enemy = self.enemy.sprite

        enemy.gravity_app()
        for sprite in self.tiles.sprites():

            if sprite.rect.colliderect(enemy.rect):
                if enemy.direction.y > 0:  # downwards collision
                    enemy.rect.bottom = sprite.rect.top
                    enemy.direction.y = 0
                    enemy.on_ground = True
                elif enemy.direction.y < 0:  # upwards collision
                    enemy.rect.top = sprite.rect.bottom
                    enemy.direction.y = 0
                    enemy.on_ceiling = True

            if enemy.on_ground and enemy.direction.y < 0 or enemy.direction.y > 1:  # Player not jumping or falling
                enemy.on_ground = False
            if enemy.on_ceiling and enemy.direction.y > 0:
                enemy.on_ceiling = False

    def ehoriz_colli(self):
        enemy = self.enemy.sprite

        # Movement changes
        enemy.rect.x += enemy.direction.x * enemy.speed

        for sprite in self.tiles.sprites():

            if sprite.rect.colliderect(enemy.rect):
                if enemy.direction.x < 0:  # left collision
                    enemy.rect.left = sprite.rect.right
                    enemy.on_left = True

                    self.current_x = enemy.rect.left

                elif enemy.direction.x > 0:  # right collision
                    enemy.rect.right = sprite.rect.left
                    enemy.on_right = True

                    self.current_x = enemy.rect.right





    #Collision

    def die_screen(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        screen = pygame.display.set_mode((screen_width, screen_hegith ))
        screen.blit(self.gameover, (screen_width/2 -115, screen_hegith /2 - 33))


    def enemy_collision(self):
        enemy = self.enemy.sprite
        player = self.player.sprite

        for sprite in self.player.sprites():
            if sprite.rect.colliderect(enemy.rect):
                self.game_status = False
                self.game_restart = False


    def run(self):
        #Tiles
        self.tiles.update(self.world_shift) #Shifting the world in direction of x
        self.tiles.draw(self.display_surface) #drawing the tiles
        self.scroll_x()
        #Player
        self.player.update()
        self.horiz_colli()
        self.vertical_colli()
        self.player.draw(self.display_surface)

        #enemy
        self.enemy.update()
        self.ehoriz_colli()
        self.evertical_colli()
        self.enemy.draw(self.display_surface)

        #collision
        self.enemy_collision()



