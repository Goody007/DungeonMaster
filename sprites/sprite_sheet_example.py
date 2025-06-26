import pygame
import os
class SpriteSheet:
    """Клас для роботи зі спрайт-листами"""
    
    def __init__(self, image_path):
        """
        Ініціалізація спрайт-листа
        :param image_path: Шлях до зображення спрайт-листа
        """
        # Перевіряємо, чи існує файл
        if not os.path.isfile(image_path):
            print(f"Помилка: Файл {image_path} не знайдено")
            raise FileNotFoundError(f"Файл спрайт-листа не знайдено: {image_path}")
        
        # Завантажуємо зображення
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
            print(f"Спрайт-лист завантажено успішно: {image_path}")
        except pygame.error as e:
            print(f"ПОМИЛКА: Не вдалося завантажити спрайт-лист: {image_path}")
            print(f"Помилка: {e}")
            raise e
    
    def get_sprite(self, x, y, width, height):
        """
        Отримання окремого спрайта з листа
        :param x, y: Координати верхнього лівого кута спрайта у спрайт-листі
        :param width, height: Розміри спрайта
        :return: Вирізаний спрайт
        """
        # Створюємо нову поверхню розміром з наш спрайт
        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Копіюємо частину спрайт-листа на нову поверхню
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        
        return sprite
    
    def get_sprites_row(self, row, sprite_width, sprite_height, sprite_count, spacing=0):
        """
        Отримання рядку спрайтів з листа
        :param row: Номер рядка (починаючи з 0)
        :param sprite_width: Ширина одного спрайта
        :param sprite_height: Висота одного спрайта
        :param sprite_count: Кількість спрайтів у рядку
        :param spacing: Відстань між спрайтами у пікселях
        :return: Список спрайтів
        """
        sprites = []
        
        for i in range(sprite_count):
            # Обчислюємо x з урахуванням відступу
            x = i * (sprite_width + spacing)
            # Обчислюємо y
            y = row * (sprite_height + spacing)
            
            # Отримуємо спрайт
            sprite = self.get_sprite(x, y, sprite_width, sprite_height)
            sprites.append(sprite)
        
        return sprites
    
    def get_sprites_grid(self, start_row, start_col, rows, cols, sprite_width, sprite_height, spacing=0):
        """
        Отримання сітки спрайтів з листа
        :param start_row, start_col: Початкові координати сітки (рядок, стовпець)
        :param rows, cols: Кількість рядків і стовпців для отримання
        :param sprite_width, sprite_height: Розміри одного спрайта
        :param spacing: Відступ між спрайтами
        :return: Двовимірний список спрайтів [рядок][стовпець]
        """
        sprites_grid = []
        
        for row in range(start_row, start_row + rows):
            sprite_row = []
            
            for col in range(start_col, start_col + cols):
                # Обчислюємо координати
                x = col * (sprite_width + spacing)
                y = row * (sprite_height + spacing)
                
                # Отримуємо спрайт
                sprite = self.get_sprite(x, y, sprite_width, sprite_height)
                sprite_row.append(sprite)
            
            sprites_grid.append(sprite_row)
        
        return sprites_grid

class SpriteAnimation:
    """Клас для керування анімацією із спрайтів"""
    
    def __init__(self, sprites, frame_duration=100):
        """
        Ініціалізація анімації
        :param sprites: Список спрайтів для анімації
        :param frame_duration: Тривалість кадру в мілісекундах
        """
        self.sprites = sprites
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()
        
    def update(self):
        """Оновлення поточного кадру анімації"""
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_duration:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.sprites)
    
    def get_current_sprite(self):
        """Отримати поточний спрайт анімації"""
        if not self.sprites:
            print("ПОМИЛКА: список спрайтів порожній")
            return None
            
        if self.current_frame < 0 or self.current_frame >= len(self.sprites):
            print(f"ПОМИЛКА: індекс кадру {self.current_frame} поза межами списку ({len(self.sprites)} спрайтів)")
            self.current_frame = 0
            
        return self.sprites[self.current_frame]
    
    def reset(self):
        """Скидання анімації на перший кадр"""
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

def test_sprite_sheet():
    """Тестова функція для демонстрації роботи спрайт-листа"""
    # Ініціалізація pygame
    pygame.init()
    
    # Створення вікна
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sprite Sheet Test")
    
    # Створення годинника для контролю FPS
    clock = pygame.time.Clock()
    
    # Шлях до тестового спрайт-листа 
    # (припускаємо, що у вас є спрайт-лист player_run.png з 8 кадрами бігу)
    sprite_sheet_path = "spritesheets/enemies/enemy_spritelist.png"  # Змініть на реальний шлях
    
    try:
        # Створюємо об'єкт спрайт-листа
        sheet = SpriteSheet(sprite_sheet_path)
        
        # Отримуємо спрайти для анімації бігу (8 кадрів у рядку)
        run_sprites = sheet.get_sprites_row(0, 64, 64, 9)
        
        # Створюємо анімацію
        run_animation = SpriteAnimation(run_sprites, 100)  # 100 мс на кадр (10 FPS)
        
        # Позиція для відображення
        player_x, player_y = 400, 300
        
        # Головний цикл
        running = True
        while running:
            # Обробка подій
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # Оновлення анімації
            run_animation.update()
            
            # Очищення екрану
            screen.fill((0, 0, 0))
            
            # Отримання поточного спрайту і малювання його
            current_sprite = run_animation.get_current_sprite()
            screen.blit(current_sprite, (player_x - current_sprite.get_width()//2, 
                                        player_y - current_sprite.get_height()//2))
            
            # Оновлення екрану
            pygame.display.flip()
            
            # Обмеження FPS
            clock.tick(60)
            
    except Exception as e:
        print(f"Помилка при тестуванні спрайт-листа: {e}")
    
    # Завершення роботи Pygame
    pygame.quit()

# Запуск тесту, якщо файл виконується безпосередньо
if __name__ == "__main__":
    test_sprite_sheet()