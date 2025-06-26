import pygame

class SpriteManager:
    """Класс для централизованного управления всеми спрайтами в игре"""
    
    def __init__(self):
        # Основная группа для всех спрайтов
        self.all_sprites = pygame.sprite.Group()
        
        # Группы по типам спрайтов для удобного взаимодействия
        self.barriers = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.graves = pygame.sprite.Group()
        self.keys = pygame.sprite.Group()
        self.decoration = pygame.sprite.Group()  # Для неинтерактивных элементов
        self.players = pygame.sprite.Group()     # Для игрока (или игроков в будущем)
        
        # Словарь для быстрого доступа к группам по имени
        self.groups = {
            'all': self.all_sprites,
            'barriers': self.barriers,
            'bullets': self.bullets,
            'monsters': self.monsters,
            'graves': self.graves,
            'keys': self.keys,
            'decoration': self.decoration,
            'players': self.players
        }
    
    def add(self, sprite, *groups):
        """
        Добавляет спрайт в указанные группы и в общую группу all_sprites
        
        :param sprite: Спрайт для добавления
        :param groups: Названия групп ('barriers', 'bullets', etc.)
        """
        self.all_sprites.add(sprite)
        
        for group_name in groups:
            if group_name in self.groups:
                self.groups[group_name].add(sprite)
    
    def remove(self, sprite, *groups):
        """
        Удаляет спрайт из указанных групп
        
        :param sprite: Спрайт для удаления
        :param groups: Названия групп; если не указаны - удаляет из всех групп
        """
        if not groups:
            # Если группы не указаны, удаляем из всех групп
            for group in self.groups.values():
                group.remove(sprite)
        else:
            for group_name in groups:
                if group_name in self.groups:
                    self.groups[group_name].remove(sprite)
    
    def get_group(self, group_name):
        """Возвращает группу спрайтов по имени"""
        return self.groups.get(group_name, pygame.sprite.Group())
    
    def update(self, *args, **kwargs):
        """Обновляет все спрайты"""
        self.all_sprites.update(*args, **kwargs)
    
    def draw(self, surface):
        """Отрисовывает все спрайты на поверхности"""
        self.all_sprites.draw(surface)
    
    def empty_group(self, group_name):
        """Очищает указанную группу спрайтов"""
        if group_name in self.groups:
            # Получаем список спрайтов в группе
            sprites_to_remove = list(self.groups[group_name])
            
            # Удаляем каждый спрайт из этой группы
            for sprite in sprites_to_remove:
                self.groups[group_name].remove(sprite)
                
                # Проверяем, есть ли этот спрайт в других группах
                in_other_groups = False
                for name, group in self.groups.items():
                    if name != group_name and name != 'all' and sprite in group:
                        in_other_groups = True
                        break
                
                # Если спрайт не находится в других группах, удаляем его из all_sprites
                if not in_other_groups:
                    self.all_sprites.remove(sprite)
