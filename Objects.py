from abc import ABC, abstractmethod
import random
import Service


class AbstractObject(ABC):

    @abstractmethod
    def __init__(self, icon, position):
        self.sprite = icon
        self.position = position

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        super().__init__(icon, position)
        self.stats = stats
        self.max_hp = 100
        self.calc_max_hp()
        self.hp = self.max_hp

    def calc_max_hp(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        super().__init__(icon, position)
        self.action = action

    def interact(self, engine, hero):
        self.action(engine, hero)


class Enemy(Creature, Interactive):

    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.exp = xp
        self.action = Service.add_gold

    def interact(self, engine, hero):
        # The idea here is that:
        #   (i) Dumb units should always attack;
        #  (ii) Wise units should attack more often than average ones;
        # (iii) Hero's luck has a small positive effect.

        prob_attack = 0.5 + abs(self.stats['intelligence'] - 25) / 50
        will_attack = random.randint(0, 100) < (prob_attack * 100 - hero.stats['luck'])

        if will_attack:
            hero.hp -= self.stats['strength']
            if hero.hp <= 0:
                engine.notify("GAME OVER")
                engine.game_process = "OFF"
                return
        hero.exp += self.exp
        for m in hero.level_up():
            engine.notify(m)
        self.action(engine, hero, coefficient=self.stats['strength'])


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_hp()
            self.hp = self.max_hp


# Decorator for magical effects
class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    # position
    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    # level
    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    # gold
    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    # hp
    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = min(value, self.base.max_hp)

    # max_hp
    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    # exp
    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    # sprite
    @property
    def sprite(self):
        return self.base.sprite

    # apply_effect to be defined for each effect
    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    # Berserk makes you strong and dumb.

    def apply_effect(self):
        self.hp = self.base.hp + 50
        self.stats["strength"] += 10
        self.stats["endurance"] += 10
        self.stats["intelligence"] = 1
        self.stats["luck"] += 3


class Blessing(Effect):
    # Blessing improves everything just a bit.

    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2


class Weakness(Effect):
    # Weakness makes you considerably less strong.

    def apply_effect(self):
        self.stats["strength"] -= 5
        self.stats["endurance"] -= 4
        self.stats["intelligence"] += 0
        self.stats["luck"] -= 1


class Pickpocket(Effect):
    # You can trust no one these days.

    def apply_effect(self):
        self.gold = int((self.gold + 1) / 2)


class MagicBow(Effect):
    # Only elven masters of the past could have created such a great bow.

    def apply_effect(self):
        self.stats["strength"] += 20
        self.stats["luck"] += 5

