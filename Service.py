import pygame
import random
import yaml
import os
import Objects

OBJECT_TEXTURE = os.path.join("texture", "objects")
ENEMY_TEXTURE = os.path.join("texture", "enemies")
ALLY_TEXTURE = os.path.join("texture", "ally")


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


def reload_game(engine, hero):
    global level_list
    level_list_max = len(level_list) - 1
    engine.level += 1

    if engine.level >= level_list_max:
        engine.game_process = "OFF"
    else:
        hero.position = [1, 1]
        engine.objects = []

        generator = level_list[min(engine.level, level_list_max)]
        _map = generator['map'].get_map()

        engine.load_map(_map)
        engine.add_objects(generator['obj'].get_objects(_map))
        engine.add_hero(hero)


def restore_hp(engine, hero):
    engine.score += 0.1
    hero.hp = hero.max_hp
    engine.notify("HP restored")


def apply_blessing(engine, hero):
    if hero.gold >= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]:
        engine.score += 0.2
        hero.gold -= int(20 * 1.5**engine.level) - 2 * hero.stats["intelligence"]

        spell_seed = random.randint(0, 3)
        if spell_seed == 0:
            engine.hero = Objects.Blessing(hero)
            engine.notify("Blessing applied")
        elif spell_seed == 1:
            engine.hero = Objects.Berserk(hero)
            engine.notify("Berserk applied")
        else:
            gold0 = hero.gold
            engine.hero = Objects.Pickpocket(hero)
            engine.notify("You were pickpocketed")
            engine.notify(f"{gold0-hero.gold} gold stolen")
    else:
        engine.score -= 0.1


def provide_weapon(engine, hero):
    if hero.stats["strength"] < 40:
        engine.score += 0.2
        engine.hero = Objects.MagicBow(hero)
        engine.notify("Magic bow equipped")
    else:
        engine.score += 0.1
        engine.notify("You are strong enough already")


def remove_effect(engine, hero):
    if hero.gold >= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"] and "base" in dir(hero):
        hero.gold -= int(10 * 1.5**engine.level) - 2 * hero.stats["intelligence"]
        engine.hero = hero.base
        engine.hero.calc_max_hp()
        engine.notify("Effect removed")


def add_gold(engine, hero, coefficient=35):
    if random.randint(1, 10) == 1:
        engine.score -= 0.1
        engine.hero = Objects.Weakness(hero)
        engine.notify("You were cursed")
    else:
        gold = int(random.randint(500, 1000) * (1.1**(engine.hero.level - 1)) * (coefficient / 35))
        engine.score += gold / 1000
        hero.gold += gold
        engine.notify(f"{gold} gold added")


class MapFactory(yaml.YAMLObject):

    @classmethod
    def from_yaml(cls, loader, node):

        data = loader.construct_mapping(node)
        _map = cls.create_map()
        _obj = cls.create_objects()
        if data != {}:
            _obj.objects = data

        return {'map': _map, 'obj': _obj}

    @classmethod
    def create_map(cls):
        return cls.Map()

    @classmethod
    def create_objects(cls):
        return cls.Objects()

    @staticmethod
    def find_empty_coord(_map, _obj, x_cond=None, y_cond=None):
        x_cond = x_cond or (1, len(_map[0]) - 2)
        y_cond = y_cond or (1, len(_map) - 2)
        coord = (random.randint(*x_cond),
                 random.randint(*y_cond))
        intersect = True
        while intersect:
            intersect = False
            if _map[coord[1]][coord[0]] == wall:
                intersect = True
                coord = (random.randint(*x_cond),
                         random.randint(*y_cond))
                continue
            for obj in _obj:
                if coord == obj.position or coord == (1, 1):
                    intersect = True
                    coord = (random.randint(*x_cond),
                             random.randint(*y_cond))
        return coord


class EndMap(MapFactory):
    yaml_tag = "!end_map"

    class Map:
        def __init__(self):
            self.Map = ['00000000000000000000000000000000000000000000000000000',
                        '0                                                   0',
                        '0                                                   0',
                        '0  00000  0   0  00000         00000  0   0  0000   0',
                        '0    0    0   0  0             0      00  0  0   0  0',
                        '0    0    00000  00000         00000  0 0 0  0   0  0',
                        '0    0    0   0  0             0      0  00  0   0  0',
                        '0    0    0   0  00000         00000  0   0  0000   0',
                        '0                                                   0',
                        '0                                                   0',
                        '00000000000000000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else random.choice(floors)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            h, w = len(_map), len(_map[0])

            obj_name = 'stairs'
            prop = object_list_prob['objects'][obj_name]
            coord = (26, 5)

            self.objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))
            return self.objects


class RandomMap(MapFactory):
    yaml_tag = "!random_map"

    class Map:

        def __init__(self):
            self.Map = [[0 for _ in range(41)] for _ in range(41)]
            for i in range(41):
                for j in range(41):
                    if i == 0 or j == 0 or i == 40 or j == 40:
                        self.Map[j][i] = wall
                    else:
                        self.Map[j][i] = [wall, floor1, floor2, floor3, floor1,
                                          floor2, floor3, floor1, floor2][random.randint(0, 8)]

        def get_map(self):
            return self.Map

    class Objects:

        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            h, w = len(_map), len(_map[0])

            for obj_name in object_list_prob['objects']:
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(random.randint(0, 20)):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects


class EmptyMap(MapFactory):
    yaml_tag = "!empty_map"

    class Map:
        def __init__(self):
            self.Map = ['00000000000000000',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '0               0',
                        '00000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else random.choice(floors)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            h, w = len(_map), len(_map[0])

            obj_name = 'stairs'
            prop = object_list_prob['objects'][obj_name]
            coord = MapFactory.find_empty_coord(_map, self.objects)

            self.objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))
            return self.objects


class SpecialMap(MapFactory):
    yaml_tag = "!special_map"

    class Map:
        def __init__(self):
            self.Map = ['000000000000000000000000000000000000000',
                        '0               00          0       0 0',
                        '0     000000    0    00  00000 000  0 0',
                        '0                        00 0  0 0    0',
                        '00000    0000000000    0    0  0 00  00',
                        '0             0000   0000   0         0',
                        '0        000     00000           000000',
                        '00000      0     0     0      00000   0',
                        '000000     0   00000   0  0     0   000',
                        '0          0     0     0  0      00   0',
                        '0          0                  0   0   0',
                        '0     000000000000    0  0    0   0   0',
                        '0           0         0  0    0   0   0',
                        '0     0     0    000000  0    0   0   0',
                        '0   0 0     0    0    0  000      0   0',
                        '0   000   000000000        0          0',
                        '0     0                        0      0',
                        '0 00000             0     000000000   0',
                        '0       0000000000     0  0       0   0',
                        '0   0   0  0     0     0  0 00000 0   0',
                        '0   0      0000      000000 0     0   0',
                        '0       0        0     0000 0  0      0',
                        '000000000000000000000000000000000000000'
                        ]
            self.Map = list(map(list, self.Map))
            for i in self.Map:
                for j in range(len(i)):
                    i[j] = wall if i[j] == '0' else random.choice(floors)

        def get_map(self):
            return self.Map

    class Objects:
        def __init__(self):
            self.objects = []

        def get_objects(self, _map):
            h, w = len(_map), len(_map[0])

            objects_dict = self.objects
            self.objects = []

            # add stairs
            obj_name = 'stairs'
            prop = object_list_prob['objects'][obj_name]
            coord = MapFactory.find_empty_coord(_map, self.objects, (int(2 * w / 3), w - 2), (int(2 * h / 3), h - 2))

            self.objects.append(Objects.Ally(
                prop['sprite'], prop['action'], coord))

            # add other objects
            for obj_name in object_list_prob['objects']:
                if obj_name == 'stairs':
                    continue
                prop = object_list_prob['objects'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            # add allies
            for obj_name in object_list_prob['ally']:
                prop = object_list_prob['ally'][obj_name]
                for i in range(random.randint(prop['min-count'], prop['max-count'])):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Ally(
                        prop['sprite'], prop['action'], coord))

            # add enemies
            for obj_name in object_list_prob['enemies']:
                prop = object_list_prob['enemies'][obj_name]
                for i in range(objects_dict.get(obj_name, 0)):
                    coord = MapFactory.find_empty_coord(_map, self.objects)

                    self.objects.append(Objects.Enemy(
                        prop['sprite'], prop, prop['experience'], coord))

            return self.objects


wall = [0]
floor1 = [0]
floor2 = [0]
floor3 = [0]
floors = [floor1, floor2, floor3]


def service_init(sprite_size, full=True):
    global object_list_prob, level_list

    global wall
    global floor1
    global floor2
    global floor3

    wall[0] = create_sprite(os.path.join("texture", "wall.png"), sprite_size)
    floor1[0] = create_sprite(os.path.join("texture", "Ground_1.png"), sprite_size)
    floor2[0] = create_sprite(os.path.join("texture", "Ground_2.png"), sprite_size)
    floor3[0] = create_sprite(os.path.join("texture", "Ground_3.png"), sprite_size)

    file = open("objects.yml", "r")

    object_list_tmp = yaml.load(file.read())
    if full:
        object_list_prob = object_list_tmp

    object_list_actions = {'reload_game': reload_game,
                           'add_gold': add_gold,
                           'apply_blessing': apply_blessing,
                           'remove_effect': remove_effect,
                           'restore_hp': restore_hp,
                           'provide_weapon': provide_weapon}

    for obj in object_list_prob['objects']:
        prop = object_list_prob['objects'][obj]
        prop_tmp = object_list_tmp['objects'][obj]
        prop['sprite'][0] = create_sprite(
            os.path.join(OBJECT_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for ally in object_list_prob['ally']:
        prop = object_list_prob['ally'][ally]
        prop_tmp = object_list_tmp['ally'][ally]
        prop['sprite'][0] = create_sprite(
            os.path.join(ALLY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)
        prop['action'] = object_list_actions[prop_tmp['action']]

    for enemy in object_list_prob['enemies']:
        prop = object_list_prob['enemies'][enemy]
        prop_tmp = object_list_tmp['enemies'][enemy]
        prop['sprite'][0] = create_sprite(
            os.path.join(ENEMY_TEXTURE, prop_tmp['sprite'][0]), sprite_size)

    file.close()

    if full:
        file = open("levels.yml", "r")
        level_list = yaml.load(file.read())['levels']
        level_list.append({'map': EndMap.Map(), 'obj': EndMap.Objects()})
        file.close()
