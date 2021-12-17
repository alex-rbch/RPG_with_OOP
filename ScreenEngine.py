import pygame
import collections
import Service
import Objects
import math

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
    "oak": (76, 46, 0, 255),
    "golden": (255, 215, 0),
    "purple": (128, 0, 128),
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        if self.successor is not None:
            return self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def calculate_left_corner(self):
        screen_shape = list(self.get_size())
        screen_shape[0] /= self.engine.sprite_size
        screen_shape[1] /= self.engine.sprite_size
        hero_pos = self.engine.hero.position
        h, w = len(self.engine.map), len(self.engine.map[0])

        draw_x = min(max(0, hero_pos[0] - screen_shape[0] / 2), w - screen_shape[0])
        draw_y = min(max(0, hero_pos[1] - screen_shape[1] / 2), h - screen_shape[1])
        return draw_x, draw_y

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw_hero(self):
        self.engine.hero.draw(self)

    def draw_map(self):
        # calculate (min_x, min_y) - left top corner
        min_x, min_y = self.calculate_left_corner()
        step_x, step_y = -int((min_x % 1) * self.engine.sprite_size), -int((min_y % 1) * self.engine.sprite_size)
        min_x, min_y = int(min_x), int(min_y)

        if self.engine.map:
            for x in range(len(self.engine.map[0]) - min_x):
                for y in range(len(self.engine.map) - min_y):
                    self.blit(self.engine.map[min_y + y][min_x + x][0],
                              (step_x + x * self.engine.sprite_size,
                               step_y + y * self.engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        # calculate (min_x, min_y) - left top corner
        min_x, min_y = self.calculate_left_corner()
        step_x, step_y = -int((min_x % 1) * self.engine.sprite_size), -int((min_y % 1) * self.engine.sprite_size)
        min_x, min_y = int(min_x), int(min_y)

        self.blit(sprite, (step_x + (coord[0] - min_x) * self.engine.sprite_size,
                           step_y + (coord[1] - min_y) * self.engine.sprite_size))

    def draw(self, canvas):
        # calculate (min_x, min_y) - left top corner
        min_x, min_y = self.calculate_left_corner()
        step_x, step_y = -int((min_x % 1) * self.engine.sprite_size), -int((min_y % 1) * self.engine.sprite_size)
        min_x, min_y = int(min_x), int(min_y)

        self.draw_map()
        for obj in self.engine.objects:
            self.blit(obj.sprite[0], (step_x + (obj.position[0] - min_x) * self.engine.sprite_size,
                                      step_y + (obj.position[1] - min_y) * self.engine.sprite_size))
        self.draw_hero()

        # draw next surface in chain
        super().draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["wooden"])
        pygame.draw.rect(self, colors["black"], (50, 30, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (50, 70, 200, 30), 2)

        pygame.draw.rect(self,
                         colors["red"],
                         (50, 30, 200 * self.engine.hero.hp / self.engine.hero.max_hp, 30))
        pygame.draw.rect(self,
                         colors["green"],
                         (50, 70, 200 * self.engine.hero.exp / (100 * (2**(self.engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("comicsansms", 20)
        self.blit(font.render(f'Hero at {self.engine.hero.position}', True, colors["black"]),
                  (250, 0))
        self.blit(font.render(f'{self.engine.level} floor', True, colors["black"]),
                  (10, 0))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (10, 30))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (10, 70))

        self.blit(font.render(f'{self.engine.hero.hp}/{self.engine.hero.max_hp}', True, colors["black"]),
                  (60, 30))
        self.blit(font.render(f'{self.engine.hero.exp}/{(100*(2**(self.engine.hero.level-1)))}', True, colors["black"]),
                  (60, 70))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (300, 30))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (300, 70))

        self.blit(font.render(f'{self.engine.hero.level}', True, colors["black"]),
                  (360, 30))
        self.blit(font.render(f'{self.engine.hero.gold}', True, colors["black"]),
                  (360, 70))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (420, 30))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (420, 70))

        self.blit(font.render(f'{self.engine.hero.stats["strength"]}', True, colors["black"]),
                  (480, 30))
        self.blit(font.render(f'{self.engine.hero.stats["luck"]}', True, colors["black"]),
                  (480, 70))

        self.blit(font.render(f'SCORE', True, colors["black"]),
                  (550, 30))
        self.blit(font.render(f'{self.engine.score:.4f}', True, colors["black"]),
                  (550, 70))

        # draw next surface in chain
        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 25
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["wooden"])

        font = pygame.font.SysFont("comicsansms", 10)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        # draw next surface in chain
        super().draw(canvas)

    def connect_engine(self, engine):
        self.engine = engine
        engine.subscribe(self)
        super().connect_engine(engine)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" → ", "Move Right"])
        self.data.append([" ← ", "Move Left"])
        self.data.append([" ↑ ", "Move Up"])
        self.data.append([" ↓ ", "Move Down"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        size = self.get_size()
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        # draw next surface in chain
        super().draw(canvas)


class StatusWindow(ScreenHandle):

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.engine.game_process in ["PAUSE", "OFF"]:
            alpha = 128
        self.fill((0, 0, 0, alpha))

        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("courier", 40)
        if self.engine.game_process in ["PAUSE", "OFF"]:
            self.fill((0, 0, 0, alpha))
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)

            if self.engine.game_process == "PAUSE":
                self.blit(font2.render("PAUSE", True, ((128, 128, 255))),
                          (280, 20))
                self.blit(font1.render("Press 'P' to pause/continue", True, ((128, 128, 255))),
                          (50, 80))

            if self.engine.game_process == "OFF":
                if self.engine.hero.hp <= 0:
                    self.blit(font2.render("GAME OVER", True, ((128, 128, 255))),
                              (240, 20))
                else:
                    self.blit(font2.render("VICTORY", True, ((128, 128, 255))),
                              (260, 20))


                self.blit(font1.render("Press 'R' to restart", True, ((128, 128, 255))),
                          (50, 80))

        # draw next surface in chain
        super().draw(canvas)


class MiniMap(ScreenHandle):

    def connect_engine(self, engine):
        self.engine = engine
        super().connect_engine(engine)

    @staticmethod
    def get_rect(position, start_position=(0, 0), step=3):
        return start_position[0] + position[0] * step, start_position[1] + position[1] * step, step, step

    def draw(self, canvas):
        self.fill(colors["wooden"])

        _map = self.engine.map
        h, w = len(_map), len(_map[0])
        step = min(int(160 / w), int(120 / h))
        start_position = (int((160 - w * step) / 2), int((120 - h * step) / 2))

        pygame.draw.rect(self, colors["black"], (start_position[0], start_position[1], w * step, h * step), 2)

        for x in range(w):
            for y in range(h):
                if _map[y][x] == Service.wall:
                    pygame.draw.rect(self, colors["black"], self.get_rect((x, y), start_position, step))

        for obj in self.engine.objects:
            selected_color = "white"
            if isinstance(obj, Objects.Ally):
                selected_color = "green"
                if obj.action == Service.reload_game:
                    selected_color = "white"
                if obj.action == Service.add_gold:
                    selected_color = "purple"
            elif isinstance(obj, Objects.Enemy):
                selected_color = "red"
            pygame.draw.rect(self, selected_color, self.get_rect(obj.position, start_position, step))

        pygame.draw.rect(self, colors["blue"], self.get_rect(self.engine.hero.position, start_position, step))
        super().draw(canvas)
