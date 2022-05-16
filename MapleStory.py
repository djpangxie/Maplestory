import pygame
import random
import Sprites

pygame.init()
screen = pygame.display.set_mode((1024, 670))


def game(cursor, gender):
    pygame.display.set_caption("Mini MapleStory")
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    boss = Sprites.BossMonster(screen)
    player = Sprites.Player(screen, gender)
    effect = Sprites.Attack(screen)
    label = Sprites.Label(screen, 5000, 0, 1)
    npc = Sprites.NPC()
    maps = Sprites.Map(screen)
    border = Sprites.Border()
    tracker = Sprites.Button('',(screen.get_width()-100,30),24,(255,255,255),True)
    healthPointBar = Sprites.HPBar(screen)
    portal = Sprites.Portal(screen)
    reminder = Sprites.Reminder()
    monsters = []
    for i in range(8):
        monsters.append(Sprites.Monster(screen,random.randrange(-1,2)))
    golds = []
    for i in range(8):
        golds.append(Sprites.Gold(screen,False))    
    golds.append(Sprites.Gold(screen,True))
    damages = []
    for i in range(8):
        damages.append(Sprites.Damage(1))
    damages.append(Sprites.Damage(0))
    damages.append(Sprites.Damage(0))
    damages.append(Sprites.Damage(2))
    mapMovementGroup = pygame.sprite.Group(monsters, player, golds, npc, damages, boss, portal)
    resetGroup = pygame.sprite.Group(healthPointBar, boss, maps, player, npc, label, monsters, portal)
    allSprites = pygame.sprite.OrderedUpdates(maps, border, tracker, healthPointBar, boss, monsters, player, effect, damages, golds, label, npc, portal, reminder, cursor)
    monster1 = pygame.mixer.Sound('./Sound Effects/OrangeMushroomDie.wav')
    monster1.set_volume(0.4)
    monster2 = pygame.mixer.Sound('./Sound Effects/Leprechaun1Die.wav')
    monster2.set_volume(0.2)
    monster3 = pygame.mixer.Sound('./Sound Effects/JrBalrogDie.wav')
    monster3.set_volume(0.3)
    monster4 = pygame.mixer.Sound('./Sound Effects/WyvernDie.wav')
    monster4.set_volume(0.4)
    monster_sound_effects = (monster1,monster2,monster3,monster4)
    boss_sound_effects = []
    for i in range(1,5):
        boss_sound = pygame.mixer.Sound('./Sound Effects/boss'+str(i)+'.wav')
        boss_sound.set_volume(1.0)
        boss_sound_effects.append(boss_sound)
    attack_sound = pygame.mixer.Sound('./Sound Effects/DarkImpaleUse.wav')
    attack_sound.set_volume(0.15)            
    heal = pygame.mixer.Sound('./Sound Effects/Red Potion.wav')
    heal.set_volume(0.8)
    gold_sound = pygame.mixer.Sound('./Sound Effects/Gold.wav')
    gold_sound.set_volume(0.6)
    enter = pygame.mixer.Sound("./Sound Effects/GameIn.wav")
    enter.set_volume(0.5)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    pygame.mixer.music.load('./Background music/music1.mp3')
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    keepGoing = True
    false_list = [False] * 10
    gold_list = false_list[:]
    attack_list = false_list[:]    
    player_moving_right = False
    player_moving_left = False
    counter = 0
    time = 0
    current_stage = 0
    play_sound = True
    game_over = False
    winner = False
    key_left = False
    key_right = False
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    key_left = True
                    if key_right:
                        player.moving(0)
                        player_moving_right = False
                    else:
                        player.moving(-6)
                        player_moving_left = True
                elif event.key == pygame.K_RIGHT:
                    key_right = True
                    if key_left:
                        player.moving(0)
                        player_moving_left = False
                    else:
                        player.moving(+6)
                        player_moving_right = True
                elif event.key == pygame.K_z:
                    if effect.finish() and player.attack_finished():
                        player.attacking()
                        effect.start(player.get_direction(), player.rect.center)
                        attack_sound.play()
                elif event.key == pygame.K_UP and player.rect.collidepoint(portal.rect.center):
                    enter.play()
                    if current_stage < 3:
                        gold_list = false_list[:]
                        play_sound = True
                        current_stage += 1
                        pygame.mixer.music.fadeout(3000)
                        pygame.mixer.music.load('./Background music/music' + str(current_stage + 1) + '.mp3')
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                        for sprite in resetGroup:
                            sprite.reset()
                        for gold in golds:
                            gold.reset((-100, -100), True)
                    else:
                        keepGoing = False
                        winner = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_left = False
                    if key_right:
                        player.moving(+6)
                        player_moving_right = True
                    else:
                        player.moving(0)
                        player_moving_left = False
                elif event.key == pygame.K_RIGHT:
                    key_right = False
                    if key_left:
                        player.moving(-6)
                        player_moving_left = True
                    else:
                        player.moving(0)
                        player_moving_right = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click.play()
                cursor.click()
                if npc.rect.collidepoint(event.pos):
                    mouse_over.play()
                    if label.spend_gold():
                        player.recover()
                        heal.play()
                        label.set_health_points(5000)
                        tracker.set_text('-1000￥')
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor.release()
        # if player.rect.colliderect(boss.rect) and counter % 30 == 0:
        #     damages[8].update_damage(player.rect.center, player.take_boss_damage())
        #     label.set_health_points(player.get_health_points())
        # elif pygame.sprite.spritecollide(player, monsters, False) and counter % 30 == 0:
        #     damages[9].update_damage(player.rect.center, player.take_damage())
        #     label.set_health_points(player.get_health_points())
        if boss.rect.colliderect(effect.rect) and not attack_list[8]:
            damage_boss = boss.take_damage()
            damages[10].update_damage(boss.rect.center, damage_boss)
            attack_list[8] = True
            healthPointBar.take_damage(damage_boss)
        if boss.get_status():
            boss_sound_effects[current_stage].play()
        for index in range(len(monsters)):
            if monsters[index].rect.colliderect(effect.rect) and not attack_list[index]:
                damages[index].update_damage(monsters[index].get_position(), monsters[index].take_damage())
                attack_list[index] = True
            if monsters[index].dead() and not gold_list[index]:
                monster_sound_effects[current_stage].play()
                golds[index].reset(monsters[index].get_position(), False)
                gold_list[index] = True
        for index in range(len(golds)):
            if player.rect.colliderect(golds[index].rect):
                gold_sound.play()
                value = golds[index].get_value()
                golds[index].reset((-100,-100), True)
                label.set_gold(value)   
                tracker.set_text("+"+str(value))
        if boss.dead():
            reminder.show(1)
            if play_sound:
                enter.play()
                play_sound = False
                golds[8].reset(boss.get_position(),False)
            portal.boss_killed() 
        elif player.get_health_points() <= 1500:
            reminder.show(0)
        else:
            reminder.reset()
        if player.rect.centerx > screen.get_width()/2 and player_moving_right and not maps.move(True):
            for sprite in mapMovementGroup:
                sprite.map_moving(-6)
        elif player.rect.centerx < screen.get_width()/2 and player_moving_left and not maps.move(False):
            for sprite in mapMovementGroup:
                sprite.map_moving(6)
        if player.get_health_points() <= 0:
            keepGoing = False
            game_over = True
        if counter % 30 == 0:
            attack_list = false_list[:]
        counter += 1
        time += 1
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    if winner:
        return hallOfFame(True, label.get_gold(), time/30, cursor)
    elif game_over:
        return hallOfFame(False, label.get_gold(), time/30, cursor)
    else:
        return 'quit'

def menu(cursor):
    pygame.display.set_caption("MapleStory Selection Screen")
    background = pygame.image.load('./Backgrounds/HomeScreen.jpg').convert()
    screen.blit(background,(0,0))
    button1 = Sprites.Button('START', (523, 172), 56, (150,150,170),False)
    button2 = Sprites.Button('Controls', (376, 357), 36,(150,150,170),False)
    button3 = Sprites.Button('About', (615, 360), 36,(150,150,170),False)
    button4 = Sprites.Button('Quit', (153, 403), 36, (150,150,170),False)
    buttonlist = [button1, button2,button3, button4]
    allSprites = pygame.sprite.OrderedUpdates(buttonlist, cursor)
    enter = pygame.mixer.Sound("./Sound Effects/GameIn.wav")
    enter.set_volume(0.5)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor.click()
                click.play()
                if button1.rect.collidepoint(event.pos):
                    enter.play()
                    return 'start'
                elif button2.rect.collidepoint(event.pos):
                    page_flip.play()
                    return 'instructions'
                elif button3.rect.collidepoint(event.pos):
                    page_flip.play()
                    return 'about'
                elif button4.rect.collidepoint(event.pos):
                    keepGoing = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor.release()
            elif event.type == pygame.MOUSEMOTION:
                for index in range(len(buttonlist)):
                    if buttonlist[index].rect.collidepoint(event.pos):
                        if not buttonlist[index].get_collide():
                            buttonlist[index].highlight()
                            mouse_over.play()
                    else:
                        buttonlist[index].normal()
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.mouse.set_visible(True)
    return 'quit'
    
def about(cursor):
    pygame.display.set_caption("About MapleStory")
    background = pygame.image.load('./Backgrounds/AboutScreen.jpg').convert()
    screen.blit(background, (0,0))
    back_button = Sprites.Button('Back to Menu', (800,360),29,(61,61,70),False)
    allSprites = pygame.sprite.Group(back_button, cursor)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                if back_button.rect.collidepoint(event.pos):
                    if not back_button.get_collide():
                        back_button.highlight()
                        mouse_over.play()
                else:
                    back_button.normal()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor.click()
                click.play()
                if back_button.rect.collidepoint(event.pos):
                    page_flip.play()
                    return 'menu'
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor.release()
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.mouse.set_visible(True)
    return 'quit'

def instructions(cursor):
    pygame.display.set_caption("Instructions")
    background = pygame.image.load('./Backgrounds/InstructionScreen.jpg').convert()
    screen.blit(background,(0,0))
    back_button = Sprites.Button('Back to Menu', (860,580),29,(61,61,70),False)
    player = Sprites.Player(screen, 1)
    allSprites = pygame.sprite.OrderedUpdates(back_button, cursor, player)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    page_flip = pygame.mixer.Sound("./Sound Effects/WorldSelect.wav")
    page_flip.set_volume(0.6)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    key_left = False
    key_right = False
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor.click()
                click.play()
                if back_button.rect.collidepoint(event.pos):
                    page_flip.play()
                    return 'menu'
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor.release()
            elif event.type == pygame.MOUSEMOTION:
                if back_button.rect.collidepoint(event.pos):
                    if not back_button.get_collide():
                        back_button.highlight()
                        mouse_over.play()
                else:
                    back_button.normal()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    key_left = True
                    if key_right:
                        player.moving(0)
                    else:
                        player.moving(-5)
                elif event.key == pygame.K_RIGHT:
                    key_right = True
                    if key_left:
                        player.moving(0)
                    else:
                        player.moving(+5)
                elif event.key == pygame.K_z:
                    player.attacking()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    key_left = False
                    if key_right:
                        player.moving(+5)
                    else:
                        player.moving(0)
                elif event.key == pygame.K_RIGHT:
                    key_right = False
                    if key_left:
                        player.moving(-5)
                    else:
                        player.moving(0)
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.mouse.set_visible(True)
    return 'quit'

def selection(cursor):
    pygame.display.set_caption("Character Selection")
    background = pygame.image.load('./Backgrounds/CharacterSelection.jpg').convert()
    screen.blit(background, (0,0))
    enter = pygame.mixer.Sound("./Sound Effects/AWizetWelcome.wav")
    enter.set_volume(0.7)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    male_button = Sprites.Button('Male', (312,407),29,(61,61,70),False)
    female_button = Sprites.Button('Female', (775,408),29,(61,61,70),False)
    other_button = Sprites.Button('Other', (540,550),29,(61,61,70),False)
    allSprites = pygame.sprite.Group(male_button, female_button, other_button, cursor)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                if male_button.rect.collidepoint(event.pos):
                    if not male_button.get_collide():
                        male_button.highlight()
                        mouse_over.play()
                else:
                    male_button.normal()
                if female_button.rect.collidepoint(event.pos):
                    if not female_button.get_collide():
                        female_button.highlight()
                        mouse_over.play()
                else:
                    female_button.normal()
                if other_button.rect.collidepoint(event.pos):
                    if not other_button.get_collide():
                        other_button.highlight()
                        mouse_over.play()
                else:
                    other_button.normal()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cursor.click()
                click.play()
                if male_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    enter.play()
                    return 2
                elif female_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    enter.play()
                    return 1
                elif other_button.rect.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(5000)
                    enter.play()
                    return 3
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cursor.release()
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.mouse.set_visible(True)
    return 'quit'
        
def hallOfFame(winner, gold_collected, new_time, cursor):
    pygame.display.set_caption("Hall of Fame")
    background = pygame.image.load('./Backgrounds/HallofFame.jpg').convert()
    screen.blit(background, (0,0))
    hall_of_fame = open('HallofFame.txt', 'r')
    fastest, most_gold = hall_of_fame.readline().strip().split()
    fastest = int(fastest)
    most_gold = int(most_gold)
    if winner:
        text = 'Brave explorer, thank you for saving maple Island!' 
        text2 = 'You finished your adventure in %ds and with %d gold!' % (new_time, gold_collected)
        if new_time < fastest:
            fastest = new_time
        if gold_collected > most_gold:
            most_gold = gold_collected
        hall_of_fame = open('HallofFame.txt', 'w')
        hall_of_fame.write(str(fastest) + ' ' + str(most_gold))
        hall_of_fame.close()
    else:
        text = 'Thank you for your attempt to save Maple Island.'
        text2 = 'You managed to collect %d gold, and survived for %ds' % (gold_collected,new_time)
    label1 = Sprites.Button(text, (514,200),23,(61,61,70),False)
    label2 = Sprites.Button(text2, (514,250), 23, (61,61,70),False)
    label3 = Sprites.Button("Fastest time: %ss" % fastest, (514,350),26,(61,61,70),False)
    label4 = Sprites.Button("Most gold collected: %d" % most_gold, (514,400), 26, (61,61,70), False)
    menu_button = Sprites.Button('Back to Menu', (824,620),29,(31,31,40),False)
    allSprites = pygame.sprite.OrderedUpdates(menu_button, label1, label2, label3, label4, cursor)
    click = pygame.mixer.Sound("./Sound Effects/MouseClick.wav")
    click.set_volume(0.6)
    mouse_over = pygame.mixer.Sound("./Sound Effects/MouseOver.wav")
    mouse_over.set_volume(0.4)
    pygame.mixer.music.load('./Background music/HallofFame.mp3')
    pygame.mixer.music.set_volume(0.3)  
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    keepGoing = True
    pygame.mouse.set_visible(False)
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            elif event.type == pygame.MOUSEMOTION:
                if menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                    menu_button.highlight()
                    mouse_over.play()
                else:
                    menu_button.normal()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cursor.click()
                click.play()
                if menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                    return 'menu'
            elif event.type == pygame.MOUSEBUTTONUP:
                cursor.release()
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()
    pygame.mouse.set_visible(True)
    return 'quit'        

def main():
    cursor = Sprites.Mouse()
    finish = False
    pygame.mixer.music.load("./Background music/WelcometoMapleStory.mp3")
    pygame.mixer.music.set_volume(0.3)
    while finish != 'quit':
        pygame.mixer.music.play(-1)
        finish = menu(cursor)
        if finish == 'about':
            if about(cursor) != 'menu':
                break
        elif finish == 'instructions':
            if instructions(cursor) != 'menu':
                break
        elif finish == 'start':
            finish = selection(cursor)
            if finish in (1,2,3):
                finish = game(cursor, finish)

if __name__ == "__main__":
    main()
