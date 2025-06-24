from pygame import* 
from animation import*


run = True
window = display.set_mode((700, 500))
back = (0, 0, 0)
bg = transform.scale(image.load("background/game.png"), (700, 500))
window.fill(back)
display.set_caption("Game")

win = transform.scale(image.load('background/Winer.png'), (500, 300))
lose = transform.scale(image.load('background/Loser.png'), (500, 300))
win_fon = transform.scale(image.load('background/dungeon_menu.jpeg'), (700, 500))
fon_lose = transform.scale(image.load('background/pause_fon.png'), (700, 500))

clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def update(self):
        self.rect.x += self.x_speed


        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window.get_width():
            self.rect.right = window.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > window.get_height():
            self.rect.bottom = window.get_height()

        platforms_touched = sprite.spritecollide(self, barriers, False)

        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed < 0:                                             
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)

        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed < 0:
           for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
        
    def fire_r(self):
        bullet = Bullet("objects/arrow_r.png", 31, 5, self.rect.x + self.rect.width, (self.rect.y + self.rect.height // 2) - 7, 18)
        bullets.add(bullet)
    def fire_l(self):
        bullet = Bullet("objects/arrow_l.png", 31, 5, (self.rect.x + self.rect.width) - 50, (self.rect.y + self.rect.height // 2) - 7, -18)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed_x, speed_y):
        super().__init__(picture, w, h, x, y)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.e_left = False
        self.e_right = False
        self.e_up = False
        self.e_down = False
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.y <= 185:
            self.speed_y = 0
            self.speed_x = 2
            self.e_up = False
            self.e_right = True

        if self.rect.x >= 500:
            self.speed_x = 0
            self.speed_y = 2
            self.e_right = False
            self.e_down = True

        if self.rect.y >= 250 and self.rect.x >= 500:
            self.speed_y = 0
            self.speed_x = -2
            self.e_down = False
            self.e_left = True

        if self.rect.x <= 180 and self.rect.y >= 250:
            self.speed_x = 0
            self.speed_y = -2
            self.e_left = False
            self.e_up = True


class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def update(self):
        self.rect.x += self.speed
                    
#Scene
#r_scene = GameSprite("background/run_scene.png", 500, 700, 0, 0)
final = GameSprite("objects/furniture/door.png", 35, 42, 460, 45)
tip_1 = GameSprite("objects/tip_1.png", 350, 30, 10, 350)
tip_2 = GameSprite("objects/tip_2.png", 350, 30, 10, 400)
tip_3 = GameSprite("objects/tip_3.png", 300, 35, 10, 450)

#Player
hero = Player("sprites/hero/stay/r_stay.png", 36, 52, 10, 220, 0, 0)
# Enemies
skeleton = Enemy('sprites/enemy/up/u_run_1.png', 27, 42, 180, 185, 0, 0)

# Barriers
barrier_1 = GameSprite("background/barrier.png", 8, 140, 427, 10)
barrier_2 = GameSprite("background/barrier.png", 8, 140, 554, 10)
barrier_3 = GameSprite("background/barrier.png", 80, 33, 522, 149)
barrier_4 = GameSprite("background/barrier.png", 462, 33, 0, 149)
barrier_5 = GameSprite("background/barrier.png", 150, 33, 410, 20)
barrier_6 = GameSprite("background/barrier.png", 232, 33, 0, 300)
barrier_7 = GameSprite("background/barrier.png", 8, 140, 225, 300)
barrier_8 = GameSprite("background/barrier.png", 140, 8, 225, 420)
barrier_9 = GameSprite("background/barrier.png", 8, 140, 324, 300)
barrier_10 = GameSprite("background/barrier.png", 300, 8, 332, 300)
barrier_11 = GameSprite("background/barrier.png", 8, 140, 590, 180)
barrier_12 = GameSprite("background/barrier.png", 28, 33, 230, 387)
barrier_13 = GameSprite("background/barrier.png", 37, 33, 285, 340)
barrier_14 = GameSprite("background/barrier.png", 26, 42, 566, 187)


barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
grave = sprite.Group()
keys = sprite.Group()
monsters.add(skeleton)

barriers.add(barrier_1)
barriers.add(barrier_2)
barriers.add(barrier_3)
barriers.add(barrier_4)
barriers.add(barrier_5)
barriers.add(barrier_6)
barriers.add(barrier_7)
barriers.add(barrier_8)
barriers.add(barrier_9)
barriers.add(barrier_10)
barriers.add(barrier_11)
barriers.add(barrier_12)
barriers.add(barrier_13)
barriers.add(barrier_14)

anim_a = 0
anim_n = 0
anim_e = 0
dead_e = 0
left_run = False
right_run = False
up_run = False
down_run = False
finish = False

# Attack animation

attack_l = False
attack_r = False
e_death = False
grave_e = False
tip_2_t = False
key_flag = False
tip_3_t = False

while run:

    for e in event.get():
        if e.type == QUIT:
            run = False
        # Движение
        if e.type == KEYDOWN:
            if e.key == K_w:
                hero.y_speed = -3
                up_run = True
            if e.key == K_s:
                hero.y_speed = 3
                down_run = True                       
            if e.key == K_a:
                hero.x_speed = -3
                left_run = True

            if e.key == K_d:
                hero.x_speed = 3
                right_run = True

            if e.key == K_LEFT:
                hero.x_speed = 0
                hero.y_speed = 0
                attack_l = True

            if e.key == K_RIGHT:
                hero.x_speed = 0
                hero.y_speed = 0
                attack_r = True
        # Остановка
        if e.type == KEYUP:
            if e.key == e.key == K_w:
                hero.y_speed = 0
                up_run = False
                hero.image = transform.scale(image.load('sprites/hero/stay/u_stay.png'), (30, 52))
            if e.key == e.key == K_s:
                hero.y_speed = 0
                down_run = False
                hero.image = transform.scale(image.load('sprites/hero/stay/d_stay.png'), (30, 58))
            if e.key == e.key == K_a:
                hero.x_speed = 0
                left_run = False
                hero.image = transform.scale(image.load('sprites/hero/stay/l_stay.png'), (36, 52))
            if e.key == e.key == K_d:
                hero.x_speed = 0
                right_run = False
                hero.image = transform.scale(image.load('sprites/hero/stay/r_stay.png'), (36, 52))

    if not finish:

        window.blit(bg, (0, 0))
        final.reset()
        tip_1.reset()
        if grave_e:
            grave.draw(window)
            keys.update()
            keys.draw(window)
        hero.reset()
        barriers.draw(window)
        hero.update()
        monsters.draw(window)
        monsters.update()
        bullets.update()
        bullets.draw(window)


        # Hero animation
        if left_run:
            if anim_n == 7:
                anim_n = 0
            else:
                anim_n += 1
            h_run_res = run_left[anim_n].get_size()
            hero.image = transform.scale(run_left[anim_n], h_run_res)

        if right_run:
            if anim_n == 7:
                anim_n = 0
            else:
                anim_n += 1
            h_run_res = run_right[anim_n].get_size()
            hero.image = transform.scale(run_right[anim_n], h_run_res)

        if up_run:
            if anim_n == 7:
                anim_n = 0
            else:
                anim_n += 1
            h_run_res = run_up[anim_n].get_size()
            hero.image = transform.scale(run_up[anim_n], h_run_res)

        if down_run:
            if anim_n == 7:
                anim_n = 0
            else:
                anim_n += 1
            h_run_res = run_down[anim_n].get_size()
            hero.image = transform.scale(run_down[anim_n], h_run_res)

        # Attack animation

        if attack_l:
            if anim_a == 9:
                hero.fire_l()
            if anim_a == 11:
                anim_a = 0
                attack_l = False
            else:
                anim_a += 1
            a_res = attack_left[anim_a].get_size()
            hero.image = transform.scale(attack_left[anim_a], a_res)

        if attack_r:
            if anim_a == 9:
                hero.fire_r()
            if anim_a == 11:
                anim_a = 0
                attack_r = False
                
            else:
                anim_a += 1
            a_res = attack_right[anim_a].get_size()
            hero.image = transform.scale(attack_right[anim_a], a_res)
            

        # Enemy animation
        if skeleton.e_left:
            if anim_e == 8:
                anim_e = 0
            else:
                anim_e += 1
            e_res = e_run_left[anim_e].get_size()
            skeleton.image = transform.scale(e_run_left[anim_e], e_res)

        if skeleton.e_right:
            if anim_e == 8:
                anim_e = 0
            else:
                anim_e += 1
            e_res = e_run_right[anim_e].get_size()
            skeleton.image = transform.scale(e_run_right[anim_e], e_res)

        if skeleton.e_up:
            if anim_e == 8:
                anim_e = 0
            else:
                anim_e += 1
            e_res = e_run_up[anim_e].get_size()
            skeleton.image = transform.scale(e_run_up[anim_e], e_res)

        if skeleton.e_down:
            if anim_e == 8:
                anim_e = 0
            else:
                anim_e += 1
            e_res = e_run_down[anim_e].get_size()
            skeleton.image = transform.scale(e_run_down[anim_e], e_res)

            
        
        if e_death:
            skeleton.speed = 0
            ed_res = e_run_right[e_death].get_size()
            if e_death == 5:
                e_death = 5
                skeleton.kill()
                grave_e = True
                nx = skeleton.rect.x
                ny = skeleton.rect.y
                skeleton_f = Enemy('sprites/enemy/death/death_5.png', 27, 28, nx, ny + 18, 0, 0)
                grave.add(skeleton_f)
                key = GameSprite("objects/key.png", 16, 16, nx + 3, ny + 24)
                keys.add(key)
                tip_2_t = True
                e_death = False
                
            else:
                e_death += 1
            skeleton.image = transform.scale(e_dead[e_death], ed_res)

        if not key_flag and sprite.spritecollideany(hero, keys):
            keys.empty()
            key.rect.x = -100
            key.rect.y = -100
            key_flag = True
            tip_2.image = transform.scale(image.load("objects/tip_2_done.png"), (300, 30))
            tip_3_t = True

        for bullet in bullets:
            if sprite.spritecollideany(bullet, monsters):
                bullet.kill()
                tip_1.image = transform.scale(image.load("objects/tip_1_done.png"), (300, 30))
                e_death = True
            if sprite.spritecollideany(bullet, barriers):
                bullet.kill()

        if sprite.spritecollideany(hero, monsters):
            window.blit(fon_lose,(0, 0))
            window.blit(lose, (150, 50))
            finish = True
        if sprite.collide_rect(hero, final):
            if key_flag:
                window.blit(win_fon,(0, 0))
                window.blit(win, (150, 50))
                finish = True
        
        if tip_2_t:
            tip_2.reset()
        if tip_3_t:
            tip_3.reset()


            

    clock.tick(15)
    display.update()