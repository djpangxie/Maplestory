import pygame
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, integer):
        super().__init__()
        self.__resting_right = []
        for i in range(4):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/stand2_' + str(i) + '.png').convert_alpha()
            self.__resting_right.append(self.__temp_image)
        self.__resting_left = []
        for i in range(4):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/stand1_' + str(i) + '.png').convert_alpha()
            self.__resting_left.append(self.__temp_image)
        self.__walking_right = []
        for i in range(4):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/walk2_' + str(i) + '.png').convert_alpha()
            self.__walking_right.append(self.__temp_image)
        self.__walking_left = []
        for i in range(4):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/walk1_' + str(i) + '.png').convert_alpha()
            self.__walking_left.append(self.__temp_image)
        self.__attacking_right = []
        for i in range(3):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/swing2_' + str(i) + ".png").convert_alpha()
            self.__attacking_right.append(self.__temp_image)
        self.__attacking_left = []
        for i in range(3):
            self.__temp_image = pygame.image.load(
                './Player' + str(integer) + '/swing1_' + str(i) + ".png").convert_alpha()
            self.__attacking_left.append(self.__temp_image)
        self.__jumping_right = pygame.image.load('./Player' + str(integer) + '/jump2_0.png').convert_alpha()
        self.__jumping_left = pygame.image.load('./Player' + str(integer) + '/jump_0.png').convert_alpha()
        self.image = self.__resting_right[0]
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.bottom = screen.get_height() - 72
        self.real_rect = self.image.get_bounding_rect()
        self.real_rect.center = self.rect.center
        self.__health_points = 5000
        self.__dy = -17.5
        self.__dx = 0
        self.__counter = 0
        self.__index = 1
        self.__jumping = False
        self.__facing_right = True
        self.__walking = False
        self.__resting = True
        self.__attacking = False
        self.__attack_finish = True
        self.__screen = screen
        self.__map_moving = False
        self.__move = 0

    def get_health_points(self):
        return self.__health_points

    def get_direction(self):
        if self.__facing_right:
            return 2
        else:
            return 1

    def recover(self):
        self.__health_points = 5000

    def jump(self):
        if not self.__jumping:
            self.__dy = -17.5
            self.__jumping = True
            self.__resting = False
            self.rect.bottom = self.__screen.get_height() - 79

    def attacking(self):
        if not self.__attacking:
            self.__index = -1
            self.__counter = 0
            self.__attacking = True
            self.__resting = False
            self.__attack_finish = False

    def attack_finished(self):
        if self.__attack_finish:
            return True
        return False

    def moving(self, integer):
        self.__resting = False
        self.__walking = True
        self.__dx = integer
        if not self.__attacking:
            self.__counter = 0
        if integer > 0:
            self.__facing_right = True
            self.image = self.__walking_right[0]
        elif integer < 0:
            self.__facing_right = False
            self.image = self.__walking_left[0]
        else:
            self.__walking = False
            if not self.__jumping and not self.__attacking:
                self.__resting = True
                if self.__facing_right:
                    self.image = self.__resting_right[0]
                else:
                    self.image = self.__resting_left[0]

    def reset(self):
        '''This method will reset the position of the player to the
        bottom left of the screen. This method returns nothing'''
        self.rect.left = 20
        self.rect.bottom = self.__screen.get_height() - 72

    def take_damage(self):
        self.__take_damage = random.randrange(100, 401)
        self.__health_points -= self.__take_damage
        return self.__take_damage

    def take_boss_damage(self):
        self.__take_damage = random.randrange(500, 1000)
        self.__health_points -= self.__take_damage
        return self.__take_damage

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def update(self):
        self.__counter += 1
        if self.__jumping:
            if not self.__attacking:
                if self.__facing_right:
                    self.image = self.__jumping_right
                elif not self.__facing_right:
                    self.image = self.__jumping_left
            if self.rect.bottom <= self.__screen.get_height() - 72:
                self.rect.bottom += self.__dy
                self.__dy += 1.75
            else:
                self.rect.bottom = self.__screen.get_height() - 72
                self.__jumping = False
                if not self.__attacking:
                    self.__counter = 0
                    if not self.__walking:
                        self.__resting = True
                        if self.__facing_right:
                            self.image = self.__resting_right[0]
                        else:
                            self.image = self.__resting_left[0]

        if self.__walking and not self.__attacking:
            if (self.real_rect.left > 0 and self.__dx < 0) or (
                    self.real_rect.right < self.__screen.get_width() and self.__dx > 0):
                self.rect.centerx += self.__dx
            if self.__facing_right and not self.__jumping and self.__counter % 4 == 0:
                try:
                    self.__index += 1
                    self.image = self.__walking_right[self.__index]
                except IndexError:
                    self.__index = 0
                    self.image = self.__walking_right[0]
                self.__counter = 0
            elif not self.__facing_right and not self.__jumping and self.__counter % 4 == 0:
                try:
                    self.__index += 1
                    self.image = self.__walking_left[self.__index]
                except IndexError:
                    self.__index = 0
                    self.image = self.__walking_left[0]
                self.__counter = 0

        if self.__resting and not self.__walking:
            if self.__facing_right and self.__counter % 12 == 0:
                try:
                    self.__index += 1
                    self.image = self.__resting_right[self.__index]
                except IndexError:
                    self.__index = 0
                    self.image = self.__resting_right[0]
                self.__counter = 0
            elif not self.__facing_right and self.__counter % 12 == 0:
                try:
                    self.__index += 1
                    self.image = self.__resting_left[self.__index]
                except IndexError:
                    self.__index = 0
                    self.image = self.__resting_left[0]
                self.__counter = 0

        if self.__attacking:
            if self.__facing_right and self.__counter % 4 == 0:
                try:
                    self.__index += 1
                    self.image = self.__attacking_right[self.__index]
                except IndexError:
                    self.__index = -1
                    self.__attack_finish = True
                    self.__attacking = False
                    if self.__walking:
                        self.image = self.__walking_right[0]
                    elif not self.__jumping:
                        self.__resting = True
                        self.image = self.__resting_right[0]
                self.__counter = 0
            elif not self.__facing_right and self.__counter % 4 == 0:
                try:
                    self.__index += 1
                    self.image = self.__attacking_left[self.__index]
                except IndexError:
                    self.__index = -1
                    self.__attack_finish = True
                    self.__attacking = False
                    if self.__walking:
                        self.image = self.__walking_left[0]
                    elif not self.__jumping:
                        self.__resting = True
                        self.image = self.__resting_left[0]
                self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
        self.real_rect = self.image.get_bounding_rect()
        self.real_rect.center = self.rect.center


class Monster(pygame.sprite.Sprite):
    def __init__(self, screen, integer):
        super().__init__()
        self.__moving1 = []
        for i in range(3):
            self.__temp_image = pygame.image.load(
                './Monster1/move' + str(integer + 1) + '_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0, 255, 0))
            self.__moving1.append(self.__temp_image)
        self.__dying1 = []
        for i in range(3):
            self.__temp_image = pygame.image.load('./Monster1/die' + str(integer + 1) + '_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0, 255, 0))
            self.__dying1.append(self.__temp_image)
        if integer != 0:
            self.__moving2 = []
            for i in range(25):
                self.__temp_image = pygame.image.load(
                    './Monster2/stand' + str(integer + 1) + '_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((255, 171, 166))
                self.__moving2.append(self.__temp_image)
        else:
            self.__moving2 = []
            for i in range(8):
                self.__temp_image = pygame.image.load(
                    './Monster2/attack' + str(integer + 1) + '_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((255, 171, 166))
                self.__moving2.append(self.__temp_image)
        self.__dying2 = []
        for i in range(17):
            self.__temp_image = pygame.image.load('./Monster2/die' + str(integer + 1) + '_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 171, 166))
            self.__dying2.append(self.__temp_image)
        if integer == 0:
            self.__moving3 = []
            for i in range(17):
                self.__temp_image = pygame.image.load(
                    './Monster3/attack' + str(integer + 1) + '_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((150, 150, 150))
                self.__moving3.append(self.__temp_image)
        else:
            self.__moving3 = []
            for i in range(5):
                self.__temp_image = pygame.image.load(
                    './Monster3/move' + str(integer + 1) + '_' + str(i) + '.png').convert()
                self.__temp_image.set_colorkey((150, 150, 150))
                self.__moving3.append(self.__temp_image)
        self.__dying3 = []
        for i in range(3):
            self.__temp_image = pygame.image.load('./Monster3/die' + str(integer + 1) + '_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150, 150, 150))
            self.__dying3.append(self.__temp_image)
        self.__attacking_left4 = []
        for i in range(36):
            self.__temp_image = pygame.image.load('./Monster4/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200, 200, 255))
            self.__attacking_left4.append(self.__temp_image)
        self.__attacking_right4 = []
        for i in range(36):
            self.__temp_image = pygame.image.load('./Monster4/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200, 200, 255))
            self.__attacking_right4.append(self.__temp_image)
        self.__dying_left4 = []
        for i in range(5):
            self.__temp_image = pygame.image.load('./Monster4/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200, 200, 255))
            self.__dying_left4.append(self.__temp_image)
        self.__dying_right4 = []
        for i in range(5):
            self.__temp_image = pygame.image.load('./Monster4/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((200, 200, 255))
            self.__dying_right4.append(self.__temp_image)
        self.__moving = self.__moving1
        self.__dying = self.__dying1
        self.image = self.__moving[0]
        self.__map_dimensions = [1775, 1700, 1683, 1975]
        self.rect = self.image.get_rect()
        self.rect.right = random.randrange(250, self.__map_dimensions[0])
        if integer == 0:
            self.rect.bottom = screen.get_height() - 60
        else:
            self.rect.bottom = screen.get_height() - 70
        self.__health_points = 3000
        self.__take_damage = 0
        self.__dead = False
        self.__finished = False
        self.__going_left = True
        self.__screen = screen
        self.__current_monster = 1
        self.__counter = 0
        self.__counter_list1 = [6, 4, 6, 3]
        self.__counter_list2 = [4, 3, 10, 6]
        self.__index = random.randrange(-1, 2)
        self.__dying_index = -1
        self.__dx = integer
        self.__dy = 0
        self.__map_moving = False
        self.__move = 0

    def take_damage(self):
        self.__take_damage = random.randrange(200, 1000)
        self.__health_points -= self.__take_damage
        return self.__take_damage

    def reset(self):
        self.__current_monster += 1
        self.__finished = False
        self.__dead = False
        self.__dying_index = -1
        if self.__current_monster == 2:
            self.__moving = self.__moving2
            self.__dying = self.__dying2
            if self.__dx != 0:
                self.__index = random.randrange(-1, 24)
            else:
                self.__index = random.randrange(-1, 7)
            self.__health_points = 4000
        elif self.__current_monster == 3:
            self.__moving = self.__moving3
            self.__dying = self.__dying3
            if self.__dx == 0:
                self.__index = random.randrange(-1, 15)
            else:
                self.__dx *= 2
                self.__index = random.randrange(-1, 4)
            self.__health_points = 5000
        elif self.__current_monster == 4:
            go_left = random.randrange(2)
            multiple = random.randrange(1, 4)
            if go_left == 0:
                self.__going_left = True
                self.__dx = -1 * multiple
            else:
                self.__going_left = False
                self.__dx = 1 * multiple
            if self.__going_left:
                self.__moving = self.__attacking_left4
                self.__dying = self.__dying_left4
            else:
                self.__moving = self.__attacking_right4
                self.__dying = self.__dying_right4
            self.__index = random.randrange(-1, 35)
            self.__dy = -1 * multiple
            self.__health_points = 7000
        self.image = self.__moving[0]
        self.rect = self.image.get_rect()
        self.rect.right = random.randrange(250, self.__map_dimensions[self.__current_monster - 1])
        if self.__current_monster == 4:
            self.rect.top = random.randrange(0, self.__screen.get_height() - 300)
        elif self.__current_monster == 2:
            if self.__dx == 0:
                self.rect.bottom = self.__screen.get_height() - 60
            else:
                self.rect.bottom = self.__screen.get_height() - 70
        else:
            self.rect.bottom = self.__screen.get_height() - 70

    def get_position(self):
        return self.rect.center

    def dead(self):
        if self.__dead:
            return True
        return False

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def update(self):
        if self.__health_points <= 0:
            self.__dead = True
        if self.__finished:
            self.rect.center = (1500, 0)
        if self.__counter % self.__counter_list1[self.__current_monster - 1] == 0 and not self.__dead:
            if self.__current_monster != 4:
                try:
                    self.__index += 1
                    self.image = self.__moving[self.__index]
                except IndexError:
                    self.__index = 0
                if self.rect.left > 0 and self.__dx < 0:
                    self.rect.left += 3 * self.__dx
                elif self.rect.right < self.__screen.get_width() and self.__dx > 0:
                    self.rect.left += 3 * self.__dx
            else:
                try:
                    self.__index += 1
                    if self.__going_left:
                        self.image = self.__attacking_left4[self.__index]
                    else:
                        self.image = self.__attacking_right4[self.__index]
                except IndexError:
                    self.__index = 0
                if ((self.rect.left > 0) and (self.__dx < 0)) or (
                        (self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
                    self.rect.left += 3 * self.__dx
                else:
                    self.__dx *= -1
                    self.__going_left = not self.__going_left
                if ((self.rect.top > 0) and (self.__dy > 0)) or (
                        (self.rect.bottom < self.__screen.get_height() - 70) and (self.__dy < 0)):
                    self.rect.top -= 3 * self.__dy
                else:
                    self.__dy *= -1
            self.__counter = 0
        if self.__counter % self.__counter_list2[self.__current_monster - 1] == 0 and self.__dead:
            try:
                self.__dying_index += 1
                if self.__current_monster != 4:
                    self.image = self.__dying[self.__dying_index]
                else:
                    if self.__going_left:
                        self.image = self.__dying_left4[self.__dying_index]
                    else:
                        self.image = self.__dying_right4[self.__dying_index]
            except IndexError:
                self.__finished = True
                self.__dead = False
            self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
        self.__counter += 1


class BossMonster(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.__going_left1 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss1/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__going_left1.append(self.__temp_image)
        self.__going_right1 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss1/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__going_right1.append(self.__temp_image)
        self.__dying_left1 = []
        for i in range(6):
            self.__temp_image = pygame.image.load('./Boss1/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__dying_left1.append(self.__temp_image)
        self.__dying_right1 = []
        for i in range(6):
            self.__temp_image = pygame.image.load('./Boss1/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__dying_right1.append(self.__temp_image)
        self.__going_left2 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss2/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 186, 92))
            self.__going_left2.append(self.__temp_image)
        self.__going_right2 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss2/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 186, 92))
            self.__going_right2.append(self.__temp_image)
        self.__dying_left2 = []
        for i in range(21):
            self.__temp_image = pygame.image.load('./Boss2/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 224, 255))
            self.__dying_left2.append(self.__temp_image)
        self.__dying_right2 = []
        for i in range(21):
            self.__temp_image = pygame.image.load('./Boss2/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 224, 255))
            self.__dying_right2.append(self.__temp_image)
        self.__going_left3 = []
        for i in range(16):
            self.__temp_image = pygame.image.load('./Boss3/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150, 150, 150))
            self.__going_left3.append(self.__temp_image)
        self.__going_right3 = []
        for i in range(16):
            self.__temp_image = pygame.image.load('./Boss3/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150, 150, 150))
            self.__going_right3.append(self.__temp_image)
        self.__dying_left3 = []
        for i in range(10):
            self.__temp_image = pygame.image.load('./Boss3/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150, 150, 150))
            self.__dying_left3.append(self.__temp_image)
        self.__dying_right3 = []
        for i in range(10):
            self.__temp_image = pygame.image.load('./Boss3/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((150, 150, 150))
            self.__dying_right3.append(self.__temp_image)
        self.__going_left4 = []
        for i in range(29):
            self.__temp_image = pygame.image.load('./Boss4/attack1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__going_left4.append(self.__temp_image)
        self.__going_right4 = []
        for i in range(29):
            self.__temp_image = pygame.image.load('./Boss4/attack2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 166))
            self.__going_right4.append(self.__temp_image)
        self.__dying_left4 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss4/die1_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 217))
            self.__dying_left4.append(self.__temp_image)
        self.__dying_right4 = []
        for i in range(11):
            self.__temp_image = pygame.image.load('./Boss4/die2_' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((255, 255, 217))
            self.__dying_right4.append(self.__temp_image)
        self.__going_left = self.__going_left1
        self.__going_right = self.__going_right1
        self.__dying_left = self.__dying_left1
        self.__dying_right = self.__dying_right1
        self.image = self.__going_left[0]
        self.__map_dimensions = [1775, 1700, 1683, 1975]
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.__map_dimensions[0], screen.get_height() - 70)
        self.__health_points = 70000
        self.__take_damage = 0
        self.__finished = False
        self.__dead = False
        self.__direction_left = True
        self.__counter = 0
        self.__index = 0
        self.__dying_index = -1
        self.__dx = -9
        self.__dy = 0
        self.__current_boss = 1
        self.__screen = screen
        self.__return = True
        self.__map_moving = False
        self.__move = 0
        self.__dying_position = [screen.get_height(), screen.get_height() - 50, screen.get_height() - 100,
                                 screen.get_height() - 10]
        self.__counter_list1 = [4, 3, 4, 4]
        self.__counter_list2 = [11, 6, 5, 8]

    def take_damage(self):
        self.__take_damage = random.randrange(1000, 5000)
        self.__health_points -= self.__take_damage
        return self.__take_damage

    def dead(self):
        if self.__finished:
            return True
        return False

    def get_status(self):
        if self.__dead and self.__return:
            self.__return = False
            return True
        return False

    def get_position(self):
        return self.__position

    def reset(self):
        self.__finished = False
        self.__dead = False
        self.__return = True
        self.__direction_left = True
        self.__index = 0
        self.__dying_index = -1
        self.__current_boss += 1
        if self.__current_boss == 2:
            self.__health_points = 80000
            self.__going_left = self.__going_left2
            self.__going_right = self.__going_right2
            self.__dying_left = self.__dying_left2
            self.__dying_right = self.__dying_right2
            self.__dx = -8
            self.__dy = 0
        elif self.__current_boss == 3:
            self.__health_points = 90000
            self.__going_left = self.__going_left3
            self.__going_right = self.__going_right3
            self.__dying_left = self.__dying_left3
            self.__dying_right = self.__dying_right3
            self.__dx = -10
            self.__dy = 6
        elif self.__current_boss == 4:
            self.__health_points = 100000
            self.__going_left = self.__going_left4
            self.__going_right = self.__going_right4
            self.__dying_left = self.__dying_left4
            self.__dying_right = self.__dying_right4
            self.__dx = -12
            self.__dy = 8
        self.image = self.__going_left[0]
        self.rect = self.image.get_rect()
        self.rect.bottomright = (self.__map_dimensions[self.__current_boss - 1], self.__screen.get_height() - 60)

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def update(self):
        if self.__health_points <= 0:
            self.__dead = True
            self.__counter = 0
        if self.__counter % self.__counter_list1[self.__current_boss - 1] == 0 and not self.__dead:
            try:
                if self.__direction_left:
                    self.image = self.__going_left[self.__index]
                else:
                    self.image = self.__going_right[self.__index]
            except IndexError:
                self.__index = 0
            self.__index += 1
            if ((self.rect.left > 0) and (self.__dx < 0)) or (
                    (self.rect.right < self.__screen.get_width()) and (self.__dx > 0)):
                self.rect.left += self.__dx
            else:
                self.__dx *= -1
                self.__direction_left = not self.__direction_left
            if ((self.rect.top > 0) and (self.__dy > 0)) or (
                    (self.rect.bottom < self.__screen.get_height() - 70) and (self.__dy < 0)):
                self.rect.top -= self.__dy
            else:
                self.__dy *= -1
            self.__counter = 0
        if self.__counter % self.__counter_list2[self.__current_boss - 1] == 0 and self.__dead:
            self.__dying_index += 1
            self.rect.bottom = self.__dying_position[self.__current_boss - 1]
            try:
                if self.__direction_left:
                    self.image = self.__dying_left[self.__dying_index]
                else:
                    self.image = self.__dying_right[self.__dying_index]
            except IndexError:
                self.__finished = True
            self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False
        if not self.__finished:
            self.__position = self.rect.center
        else:
            self.rect.center = (-700, -100)
        self.__counter += 1


class Map(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.__list_of_images = []
        for i in range(1, 5):
            self.__temp_image = pygame.image.load('./Maps/Map_' + str(i) + '.jpg').convert()
            self.__list_of_images.append(self.__temp_image)
        self.image = self.__list_of_images[0]
        self.rect = self.image.get_rect()
        self.__map = 0
        self.__screen = screen
        self.__move = 'none'
        self.__reach_end = True

    def reset(self):
        self.__map += 1
        if self.__map < 4:
            self.image = self.__list_of_images[self.__map]
            self.rect = self.image.get_rect()

    def move(self, go_right):
        if go_right:
            self.__move = 'right'
        else:
            self.__move = 'left'
        if self.__reach_end:
            return True
        return False

    def update(self):
        if self.__move == 'right' and self.rect.right >= self.__screen.get_width() + 5:
            self.rect.right -= 6
            self.__reach_end = False
        elif self.__move == 'left' and self.rect.left <= -5:
            self.rect.left += 6
            self.__reach_end = False
        else:
            self.__reach_end = True
        self.__move = 'none'


class Gold(pygame.sprite.Sprite):
    def __init__(self, screen, boss):
        super().__init__()
        if not boss:
            self.image = pygame.image.load('./OtherImages/gold.gif').convert()
        else:
            self.image = pygame.image.load('./OtherImages/gold_sack.gif').convert()
        self.rect = self.image.get_rect()
        self.rect.center = (-100, -100)
        self.__value = 0
        self.__boss = boss
        self.__screen = screen
        self.__map_moving = False
        self.__move = 0

    def reset(self, position, set_position):
        if not set_position:
            if not self.__boss:
                self.__value = random.randrange(100, 301)
            else:
                self.__value = random.randrange(500, 1201)
            self.rect.center = (position[0], self.__screen.get_height() - 85)
        else:
            self.__value = 0
            self.rect.center = (-100, -100)

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def get_value(self):
        return self.__value

    def update(self):
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False


class Damage(pygame.sprite.Sprite):
    def __init__(self, attack_who):
        super().__init__()
        self.__font = pygame.font.Font('./Fonts/DAMAGE.TTF', 48)
        self.__list = [(255, 106, 106), (255, 50, 50), (225, 0, 54)]
        self.__colour = self.__list[attack_who]
        self.__damage = self.__font.render('0', True, self.__colour)
        self.image = self.__damage
        self.rect = self.image.get_rect()
        self.rect.center = (-200, -200)
        self.__counter = 0
        self.__map_moving = False
        self.__move = 0

    def update_damage(self, position, damage):
        self.__damage = self.__font.render(str(damage), True, self.__colour)
        self.image = self.__damage
        self.rect.midbottom = (position[0], position[1] - 20)
        self.__counter = 0

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def update(self):
        self.__counter += 1
        if self.__counter % 40 == 0:
            self.rect.center = (-200, -200)
            self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False


class HPBar(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.__hpBar = pygame.Surface((screen.get_width(), 7)).convert()
        self.__hpBar.fill((225, 0, 81))
        self.image = self.__hpBar
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 50)
        self.__list = [70000, 80000, 90000, 100000]
        self.__health = self.__list[0]
        self.__new_width = screen.get_width()
        self.__screen = screen
        self.__current_boss = 0

    def reset(self):
        self.__current_boss += 1
        self.__health = self.__list[self.__current_boss]
        self.__new_width = self.__screen.get_width()
        self.__hpBar = pygame.Surface((self.__new_width, 7)).convert()
        self.__hpBar.fill((225, 0, 81))

    def take_damage(self, damage):
        self.__new_width = self.__new_width * (self.__health - damage) / self.__health
        if self.__new_width <= 0:
            self.__new_width = 0
        self.__health -= damage
        self.__hpBar = pygame.Surface((self.__new_width, 7)).convert()
        self.__hpBar.fill((225, 0, 81))

    def update(self):
        self.image = self.__hpBar


class Attack(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.__attack_left = []
        for i in range(12):
            self.__temp_image = pygame.image.load('./Skill/effect.1_' + str(i) + '.png')
            self.__attack_left.append(self.__temp_image)
        self.__attack_right = []
        for i in range(12):
            self.__temp_image = pygame.image.load('./Skill/effect.2_' + str(i) + '.png')
            self.__attack_right.append(self.__temp_image)
        self.image = self.__attack_right[0]
        self.rect = self.image.get_rect()
        self.rect.center = (-400, 0)
        self.__index = 0
        self.__integer = 0
        self.__screen = screen
        self.__finished = True

    def finish(self):
        if self.__finished:
            return True
        return False

    def start(self, integer, position, gender):
        if gender == 3:
            self.__index = 10
        else:
            self.__index = -1
        self.__integer = integer
        self.__position = position
        self.__finished = False

    def update(self):
        if self.__integer == 1:
            try:
                self.__index += 1
                self.image = self.__attack_left[self.__index]
                self.rect.midright = (self.__position[0] + 50, self.__position[1] - 25)
            except IndexError:
                self.__integer = 0
                self.__finished = True
                self.rect.center = (-400, 0)
        elif self.__integer == 2:
            try:
                self.__index += 1
                self.image = self.__attack_right[self.__index]
                self.rect.midleft = (self.__position[0] - 50, self.__position[1] - 25)
            except IndexError:
                self.__integer = 0
                self.__finished = True
                self.rect.center = (-400, 0)


class Label(pygame.sprite.Sprite):
    def __init__(self, screen, health, amount, stage_num):
        super().__init__()
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', 32)
        self.__health_points = health
        self.__amount = amount
        self.__stage = stage_num
        self.__screen = screen
        self.__message = 'HP: %d                   STAGE: %d                   GOLD: %d   ' % (
            self.__health_points, self.__stage, self.__amount)
        self.image = self.__font.render(self.__message, True, (245, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (self.__screen.get_width() / 2, 30)

    def set_health_points(self, health):
        self.__health_points = health

    def set_gold(self, value):
        self.__amount += value

    def get_gold(self):
        return self.__amount

    def reset(self):
        self.__stage += 1

    def spend_gold(self):
        if self.__amount >= 1000:
            self.__amount -= 1000
            return True
        return False

    def update(self):
        self.__message = 'HP: %d                   STAGE: %d                   GOLD: %d   ' % (
            self.__health_points, self.__stage, self.__amount)
        self.image = self.__font.render(self.__message, True, (245, 255, 255))


class NPC(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__npc_images = []
        for i in range(12):
            self.__temp_image = pygame.image.load('./NPC/npc' + str(i) + '.png').convert()
            self.__temp_image.set_colorkey((0, 255, 0))
            self.__npc_images.append(self.__temp_image)
        self.image = self.__npc_images[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = (250, 300)
        self.__index = 0
        self.__counter = 0
        self.__map_moving = False
        self.__move = 0

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def reset(self):
        self.rect.midbottom = (250, 300)

    def update(self):
        self.__counter += 1
        if self.__counter % 10 == 0:
            self.__index += 1
            if self.__index >= 12:
                self.__index = 0
            self.image = self.__npc_images[self.__index]
            self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False


class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__normal = pygame.image.load('./OtherImages/normal.gif').convert()
        self.__normal.set_colorkey((0, 255, 0))
        self.__click = pygame.image.load('./OtherImages/click.gif').convert()
        self.__click.set_colorkey((0, 255, 0))
        self.image = self.__normal
        self.rect = self.image.get_rect()
        self.rect.center = (624, 335)

    def click(self):
        self.image = self.__click

    def release(self):
        self.image = self.__normal

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Button(pygame.sprite.Sprite):
    def __init__(self, text, position, size, colour, track):
        super().__init__()
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', size)
        self.image = self.__font.render(text, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.__message = text
        self.__colour = colour
        self.__collide = False
        self.__counter = 0
        self.__tracker = track

    def highlight(self):
        self.__collide = True

    def normal(self):
        self.__collide = False

    def get_collide(self):
        if self.__collide:
            return True
        else:
            return False

    def set_text(self, text):
        self.__message = text

    def update(self):
        if self.__collide:
            self.image = self.__font.render(self.__message, True, (255, 195, 205))
        else:
            self.image = self.__font.render(self.__message, True, self.__colour)
        self.__counter += 1
        if self.__counter % 60 == 0:
            if self.__tracker:
                self.__message = ''
            self.__counter = 0


class Border(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('./OtherImages/border.jpg').convert()
        self.rect = self.image.get_rect()


class Portal(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.__list = []
        for i in range(6):
            self.__temp_image = pygame.image.load('./Portal/0_' + str(i) + '.png')
            self.__list.append(self.__temp_image)
        self.image = self.__list[0]
        self.rect = self.image.get_rect()
        self.rect.center = (0, -300)
        self.__index = 0
        self.__counter = 0
        self.__screen = screen
        self.__reset = True
        self.__dy = 0
        self.__map_moving = False
        self.__move = 0

    def boss_killed(self):
        if self.__reset:
            self.__dy = 15
            self.rect.centerx = self.__screen.get_width() - 180
            self.__reset = False

    def reset(self):
        self.rect.center = (0, -300)
        self.__reset = True
        self.__dy = 0

    def map_moving(self, integer):
        self.__map_moving = True
        self.__move = integer

    def update(self):
        self.__counter += 1
        if self.rect.bottom <= self.__screen.get_height() - 79:
            self.rect.bottom += self.__dy
        if self.__counter % 6 == 0:
            try:
                self.image = self.__list[self.__index]
                self.__index += 1
            except IndexError:
                self.__index = 0
            self.__counter = 0
        if self.__map_moving:
            self.rect.centerx += self.__move
            self.__map_moving = False


class Reminder(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__font = pygame.font.Font('./Fonts/Handwritten.ttf', 22)
        self.__messages = ['Your HP is running low. If you have 1000 gold or more, click the NPC or spacebar',
                           'You cleared the stage! Enter the portal to advance to the next stage']
        self.message = self.__messages[0]
        self.image = self.__font.render(self.__messages[0], True, (177, 177, 177))
        self.__index = 0
        self.rect = self.image.get_rect()
        self.rect.bottom = 0
        self.__show = False

    def show(self, index):
        self.__index = index
        self.__show = True

    def reset(self):
        self.__show = False

    def update(self):
        if self.__show:
            self.rect.midtop = (542, 59)
            self.image = self.__font.render(self.__messages[self.__index], True, (0, 0, 0))
        else:
            self.rect.bottom = 0
