import pygame

class ResourceManager:
    @staticmethod
    def load_image(path, size=None):
        image = pygame.image.load(path)
        if size:
            return pygame.transform.scale(image, size)
        return image

    @staticmethod
    def load_animation(paths, sizes=None):
        if sizes:
            return [pygame.transform.scale(pygame.image.load(path), sizes) for path in paths]
        return [pygame.image.load(path) for path in paths]

def load_player_animations():
    run_left = ResourceManager.load_animation([
        "Finals/hero/run/l_run_1.png", "Finals/hero/run/l_run_2.png", 
        "Finals/hero/run/l_run_3.png", "Finals/hero/run/l_run_4.png",
        "Finals/hero/run/l_run_5.png", "Finals/hero/run/l_run_6.png",
        "Finals/hero/run/l_run_7.png", "Finals/hero/run/l_run_8.png"
    ])

    run_right = ResourceManager.load_animation([
        "Finals/hero/run/r_run_1.png", "Finals/hero/run/r_run_2.png", 
        "Finals/hero/run/r_run_3.png", "Finals/hero/run/r_run_4.png",
        "Finals/hero/run/r_run_5.png", "Finals/hero/run/r_run_6.png",
        "Finals/hero/run/r_run_7.png", "Finals/hero/run/r_run_8.png"
    ])

    run_up = ResourceManager.load_animation([
        "Finals/hero/run/u_run_1.png", "Finals/hero/run/u_run_2.png", 
        "Finals/hero/run/u_run_3.png", "Finals/hero/run/u_run_4.png",
        "Finals/hero/run/u_run_5.png", "Finals/hero/run/u_run_6.png",
        "Finals/hero/run/u_run_7.png", "Finals/hero/run/u_run_8.png"
    ])

    run_down = ResourceManager.load_animation([
        "Finals/hero/run/d_run_1.png", "Finals/hero/run/d_run_2.png", 
        "Finals/hero/run/d_run_3.png", "Finals/hero/run/d_run_4.png",
        "Finals/hero/run/d_run_5.png", "Finals/hero/run/d_run_6.png",
        "Finals/hero/run/d_run_7.png", "Finals/hero/run/d_run_8.png"
    ])

    attack_right = ResourceManager.load_animation([
        "Finals/hero/attack/r_attack_1.png", "Finals/hero/attack/r_attack_2.png", 
        "Finals/hero/attack/r_attack_3.png", "Finals/hero/attack/r_attack_4.png",
        "Finals/hero/attack/r_attack_5.png", "Finals/hero/attack/r_attack_6.png",
        "Finals/hero/attack/r_attack_7.png", "Finals/hero/attack/r_attack_8.png",
        "Finals/hero/attack/r_attack_9.png", "Finals/hero/attack/r_attack_10.png",
        "Finals/hero/attack/r_attack_11.png", "Finals/hero/attack/r_attack_12.png",
        "Finals/hero/attack/r_attack_13.png"
    ])

    attack_left = ResourceManager.load_animation([
        "Finals/hero/attack/l_attack_1.png", "Finals/hero/attack/l_attack_2.png", 
        "Finals/hero/attack/l_attack_3.png", "Finals/hero/attack/l_attack_4.png",
        "Finals/hero/attack/l_attack_5.png", "Finals/hero/attack/l_attack_6.png",
        "Finals/hero/attack/l_attack_7.png", "Finals/hero/attack/l_attack_8.png",
        "Finals/hero/attack/l_attack_9.png", "Finals/hero/attack/l_attack_10.png",
        "Finals/hero/attack/l_attack_11.png", "Finals/hero/attack/l_attack_12.png",
        "Finals/hero/attack/l_attack_13.png"
    ])

    return {
        'run_left': run_left,
        'run_right': run_right,
        'run_up': run_up,
        'run_down': run_down,
        'attack_left': attack_left,
        'attack_right': attack_right,
        'stay': {
            'left': ResourceManager.load_image('Finals/hero/stay/l_stay.png', (36, 52)),
            'right': ResourceManager.load_image('Finals/hero/stay/r_stay.png', (36, 52)),
            'up': ResourceManager.load_image('Finals/hero/stay/u_stay.png', (30, 52)),
            'down': ResourceManager.load_image('Finals/hero/stay/d_stay.png', (30, 58))
        }
    }

def load_enemy_animations():
    run_left = ResourceManager.load_animation([
        "Finals/enemy/left/l_run_1.png", "Finals/enemy/left/l_run_2.png", 
        "Finals/enemy/left/l_run_3.png", "Finals/enemy/left/l_run_4.png",
        "Finals/enemy/left/l_run_5.png", "Finals/enemy/left/l_run_6.png",
        "Finals/enemy/left/l_run_7.png", "Finals/enemy/left/l_run_8.png",
        "Finals/enemy/left/l_run_9.png"
    ])

    run_right = ResourceManager.load_animation([
        "Finals/enemy/right/r_run_1.png", "Finals/enemy/right/r_run_2.png", 
        "Finals/enemy/right/r_run_3.png", "Finals/enemy/right/r_run_4.png",
        "Finals/enemy/right/r_run_5.png", "Finals/enemy/right/r_run_6.png",
        "Finals/enemy/right/r_run_7.png", "Finals/enemy/right/r_run_8.png",
        "Finals/enemy/right/r_run_9.png"
    ])

    run_up = ResourceManager.load_animation([
        "Finals/enemy/up/u_run_1.png", "Finals/enemy/up/u_run_2.png", 
        "Finals/enemy/up/u_run_3.png", "Finals/enemy/up/u_run_4.png",
        "Finals/enemy/up/u_run_5.png", "Finals/enemy/up/u_run_6.png",
        "Finals/enemy/up/u_run_7.png", "Finals/enemy/up/u_run_8.png",
        "Finals/enemy/up/u_run_9.png"
    ])

    run_down = ResourceManager.load_animation([
        "Finals/enemy/down/d_run_1.png", "Finals/enemy/down/d_run_2.png", 
        "Finals/enemy/down/d_run_3.png", "Finals/enemy/down/d_run_4.png",
        "Finals/enemy/down/d_run_5.png", "Finals/enemy/down/d_run_6.png",
        "Finals/enemy/down/d_run_7.png", "Finals/enemy/down/d_run_8.png",
        "Finals/enemy/down/d_run_9.png"
    ])

    death = ResourceManager.load_animation([
        "Finals/enemy/death/death_1.png", "Finals/enemy/death/death_2.png",
        "Finals/enemy/death/death_3.png", "Finals/enemy/death/death_4.png",
        "Finals/enemy/death/death_5.png", "Finals/enemy/death/death_6.png"
    ])

    return {
        'run_left': run_left,
        'run_right': run_right,
        'run_up': run_up,
        'run_down': run_down,
        'death': death
    }

def load_tips():
    return {
        'tip_1': ResourceManager.load_image("objects/tip_1.png", (350, 30)),
        'tip_2': ResourceManager.load_image("objects/tip_2.png", (350, 30)),
        'tip_3': ResourceManager.load_image("objects/tip_3.png", (300, 35)),
        'tip_1_done': ResourceManager.load_image("objects/tip_1_done.png", (300, 30)),
        'tip_2_done': ResourceManager.load_image("objects/tip_2_done.png", (300, 30))
    }
