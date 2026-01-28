import random
from time import sleep

WARRIORS_NAMES = [
    'Leonardo DiCaprio',
    'Scarlett Johansson',
    'Dwayne Johnson',
    'Jennifer Lawrence',
    'Tom Hanks',
    'Angelina Jolie',
    'Will Smith',
    'Emma Watson',
    'Robert Downey Jr.',
    'Beyoncé',
    'Chris Hemsworth',
    'Taylor Swift',
    'Brad Pitt',
    'Meryl Streep',
    'Ryan Reynolds',
    'Natalie Portman',
    'Keanu Reeves',
    'Sandra Bullock',
    'Julia Roberts',
    'Samuel L. Jackson',
]

print(f'Имен в списке:{len(WARRIORS_NAMES)}')

WEAPONS = [
    'Sword', 'Shield', 'Helmet', 'Nike Air', 'Armor', 'Bow', 'Arrow',
    'Spade', 'Axe', 'Mace', 'Blowfish', 'Stick', 'Ring', 'Underpants'
]

BATTLE_SPEED = 0.2


class Weapon:
    name: str
    protection: float
    damage: int

    def __init__(self, name: str, protection: float, damage: int):
        self.name = name
        self.protection = protection
        self.damage = damage

    def __str__(self):
        return f"{self.name}: DMG+{self.damage}, DEF+{self.protection:.2f}"


class Person:
    name: str
    hp: float
    weapons: list
    base_attack: int
    base_protection: float

    def __init__(self, name: str, hp: int, attack: int, protection: float):
        self.name = name
        self.hp = float(hp)
        self.base_attack = attack
        self.base_protection = float(protection)
        self.weapons = []

    def set_weapons(self, weapons: list):
        self.weapons = weapons

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name!r}, hp={self.hp}, "
                f"damage={self.base_attack}, prot={self.base_protection:.2f}, "
                f"weapons={self.weapons!r})")

    def __str__(self):
        return (f"{self.__class__.__name__} {self.name}: "
                f"HP={self.hp:.1f}, ATK={self.base_attack}, "
                f"DEF={self.base_protection:.2f}")

    def roll_crit_multiplier(self) -> int:
        if self.hp <= 50:
            random_num = random.randint(1, 10)
            if random_num == 1:
                print(f'💥 💥 💥 {self.name} activated a critical hit! 💥 💥 💥')
                return 3
        return 1


class Paladin(Person):
    def __init__(self, name, hp, base_attack, protection):
        super().__init__(name, hp, base_attack, protection)
        self.hp = float(hp * 2)
        self.base_protection = float(protection * 2)


class Warrior(Person):
    def __init__(self, name, hp, base_attack, protection):
        super().__init__(name, hp, base_attack, protection)
        self.base_attack = base_attack * 2


def damage(weapons: list, attacker: Person) -> float:
    selected_weapon = random.choice(weapons)
    crit_mult = attacker.roll_crit_multiplier()

    total_damage = (attacker.base_attack * crit_mult) + selected_weapon.damage

    print(f'Attacker {attacker.name} choose weapon for fight - {selected_weapon}')
    if crit_mult == 3:
        print(f'CRIT x3! Base ATK {attacker.base_attack} -> {attacker.base_attack * 3}')

    return float(total_damage)


def protection(weapons: list, defender: Person) -> float:
    selected_weapon = random.choice(weapons)
    total_protection = defender.base_protection + selected_weapon.protection

    print(f'Defender: {defender} choose for protection - {selected_weapon}')
    return float(total_protection)


def apply_hit(defender: Person, hit: float):
    defender.hp = round(defender.hp - hit, 1)


def generate_weapons():
    weapon_list = []
    for _ in range(20):
        name = random.choice(WEAPONS)
        prot = round(random.uniform(0.01, 2.0), 1)
        dmg = random.randint(1, 10)
        weapon_list.append(Weapon(name, prot, dmg))
    return weapon_list


def generate_person():
    person_list = []
    for name in WARRIORS_NAMES:
        hp = random.randint(1, 100)
        base_attack = random.randint(1, 10)
        prot = round(random.uniform(0.01, 1.0), 1)
        cls_warrior = random.choice([Paladin, Warrior])
        person_list.append(cls_warrior(name, hp, base_attack, prot))
    return person_list


def dress_up_warrior():
    warriors = generate_person()
    print(f"[dress_up_warrior] Сгенерировано персонажей: {len(warriors)}")

    for person in warriors:
        count = random.randint(1, 4)
        all_items = generate_weapons()
        items = random.sample(all_items, count)
        person.set_weapons(items)

    return warriors


def arena(fighters: list) -> list:
    winners = []

    while len(fighters) > 0:
        if len(fighters) < 2:
            last = fighters.pop()
            winners.append(last)
            return winners

        index1 = random.randrange(len(fighters))
        index2 = random.randrange(len(fighters))
        while index1 == index2:
            index2 = random.randrange(len(fighters))

        attacker = fighters.pop(index1)
        defender = fighters.pop(index2 if index2 < index1 else index2 - 1)

        print('__NEW fight is begin!__')
        print(f'Attacker: {attacker} \nDefender: {defender}')

        hits = 0
        while defender.hp > 0 and attacker.hp > 0:
            hits += 1

            attacker_dem = damage(attacker.weapons, attacker)
            defender_prot = protection(defender.weapons, defender)
            hit = max(0.0, attacker_dem - defender_prot)

            apply_hit(defender, hit)

            if defender.hp <= 0:
                winners.append(attacker)
                print(f'Attacker {attacker.name} is win! {defender.name} is dead from {hits} hits.')
                break
            else:
                print(f'The fight is continuing {defender.name} is alive! HP - {defender.hp:.1f}')

            sleep(BATTLE_SPEED)

            defender_dem = damage(defender.weapons, defender)
            attacker_prot = protection(attacker.weapons, attacker)
            hit = max(0.0, defender_dem - attacker_prot)

            print('Now Defender is attacking the attacker! \n')
            apply_hit(attacker, hit)

            if attacker.hp <= 0:
                winners.append(defender)
                print(f'Defender {defender.name} is win! {attacker.name} is dead from {hits} hits.')
                break
            else:
                print(f'Fight is continues {attacker.name} is alive! HP - {attacker.hp:.1f}')

    return winners


def main():
    fighters = dress_up_warrior()

    round_winners = arena(fighters)
    print('🔥 🔥 🔥 Now is a battle of winners! Fight!🔥 🔥 🔥 ')
    for w in round_winners:
        print(f'Win {w}!')

    while len(round_winners) > 1:
        round_winners = arena(round_winners)

    print(f'🏆 Champion: {round_winners[0]}')


if __name__ == '__main__':
    main()
