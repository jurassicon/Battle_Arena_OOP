import random
from dataclasses import dataclass
from time import sleep
from typing import Dict, List, Optional, Tuple


WARRIORS_NAMES = [
    "Leonardo DiCaprio",
    "Scarlett Johansson",
    "Dwayne Johnson",
    "Jennifer Lawrence",
    "Tom Hanks",
    "Angelina Jolie",
    "Will Smith",
    "Emma Watson",
    "Robert Downey Jr.",
    "Beyoncé",
    "Chris Hemsworth",
    "Taylor Swift",
    "Brad Pitt",
    "Meryl Streep",
    "Ryan Reynolds",
    "Natalie Portman",
    "Keanu Reeves",
    "Sandra Bullock",
    "Julia Roberts",
    "Samuel L. Jackson",
]

WEAPON_NAMES = [
    "Sword",
    "Shield",
    "Helmet",
    "Nike Air",
    "Armor",
    "Bow",
    "Arrow",
    "Spade",
    "Axe",
    "Mace",
    "Blowfish",
    "Stick",
    "Ring",
    "Underpants",
]

# Pause between attack actions (seconds). Set to 0 for instant battles.
BATTLE_SPEED = 0.2

# Print detailed logs for each attack action.
VERBOSE_FIGHT_LOG = True

# Safety guard for very long fights when damage frequently becomes 0.
MAX_ATTACK_ACTIONS_PER_MATCH = 200


class Weapon:
    name: str
    protection: float
    damage: int

    def __init__(self, name: str, protection: float, damage: int) -> None:
        self.name = name
        self.protection = float(protection)
        self.damage = int(damage)

    def __str__(self) -> str:
        return f"{self.name}: DMG+{self.damage}, DEF+{self.protection:.2f}"


class Person:
    name: str
    hp: float
    weapons: List["Weapon"]
    base_attack: int
    base_protection: float

    def __init__(
        self,
        name: str,
        hp: int,
        attack: int,
        protection: float,
    ) -> None:
        self.name = name
        self.hp = float(hp)
        self.base_attack = int(attack)
        self.base_protection = float(protection)
        self.weapons = []

    def set_weapons(self, weapons: List["Weapon"]) -> None:
        self.weapons = weapons

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, hp={self.hp:.1f}, "
            f"damage={self.base_attack}, prot={self.base_protection:.2f}, "
            f"weapons={self.weapons!r})"
        )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} {self.name}: "
            f"HP={self.hp:.1f}, ATK={self.base_attack}, "
            f"DEF={self.base_protection:.2f}"
        )

    def roll_crit_multiplier(self) -> int:
        """
        If hp <= 50, there is a 10% chance to activate a critical hit:
        base_attack * 3.
        """
        if self.hp <= 50 and random.randint(1, 10) == 1:
            if VERBOSE_FIGHT_LOG:
                print(
                    f"💥 💥 💥 {self.name} activated a critical hit! "
                    f"💥 💥 💥"
                )
            return 3
        return 1


class Paladin(Person):
    def __init__(
        self,
        name: str,
        hp: int,
        base_attack: int,
        protection: float,
    ) -> None:
        super().__init__(name, hp, base_attack, protection)
        self.hp = float(hp * 2)
        self.base_protection = float(protection * 2)


class Warrior(Person):
    def __init__(
        self,
        name: str,
        hp: int,
        base_attack: int,
        protection: float,
    ) -> None:
        super().__init__(name, hp, base_attack, protection)
        self.base_attack = int(base_attack * 2)


def apply_hit(defender: Person, hit: float) -> None:
    defender.hp = max(0.0, round(defender.hp - float(hit), 1))


def calc_damage(attacker: Person) -> Tuple[float, bool, Weapon]:
    """
    Returns:
      - raw_damage: (base_attack * crit_multiplier) + weapon.damage
      - is_crit
      - selected_weapon
    """
    selected_weapon = random.choice(attacker.weapons)
    crit_mult = attacker.roll_crit_multiplier()
    raw_damage = (attacker.base_attack * crit_mult) + selected_weapon.damage
    return float(raw_damage), (crit_mult == 3), selected_weapon


def calc_protection(defender: Person) -> Tuple[float, Weapon]:
    """
    Returns:
      - total_protection: base_protection + weapon.protection
      - selected_weapon
    """
    selected_weapon = random.choice(defender.weapons)
    total_protection = defender.base_protection + selected_weapon.protection
    return float(total_protection), selected_weapon


def generate_weapons() -> List[Weapon]:
    weapon_list: List[Weapon] = []
    for _ in range(20):
        name = random.choice(WEAPON_NAMES)
        prot = round(random.uniform(0.01, 2.0), 1)
        dmg = random.randint(1, 10)
        weapon_list.append(Weapon(name, prot, dmg))
    return weapon_list


def generate_person() -> List[Person]:
    person_list: List[Person] = []
    for name in WARRIORS_NAMES:
        hp = random.randint(1, 100)
        base_attack = random.randint(1, 10)
        prot = round(random.uniform(0.01, 1.0), 1)
        cls_warrior = random.choice([Paladin, Warrior])
        person_list.append(cls_warrior(name, hp, base_attack, prot))
    return person_list


def dress_up_warrior() -> List[Person]:
    warriors = generate_person()
    if VERBOSE_FIGHT_LOG:
        print(f"[dress_up_warrior] Сгенерировано персонажей: {len(warriors)}")

    for person in warriors:
        count = random.randint(1, 4)
        all_items = generate_weapons()
        items = random.sample(all_items, count)
        person.set_weapons(items)

    return warriors


@dataclass
class FighterStats:
    name: str
    cls_name: str
    fights: int = 0
    wins: int = 0
    losses: int = 0
    attacks: int = 0
    successful_hits: int = 0
    blocks: int = 0
    crits: int = 0
    damage_dealt: float = 0.0
    damage_taken: float = 0.0
    max_single_hit: float = 0.0


@dataclass
class MatchResult:
    round_no: int
    match_no: int
    a_name: str
    b_name: Optional[str]
    winner: str
    loser: Optional[str]
    attacks: int
    winner_hp: float
    loser_hp: Optional[float]
    resolved_by: str  # "ko" | "timeout" | "bye"


def get_stats(stats: Dict[str, FighterStats], p: Person) -> FighterStats:
    if p.name not in stats:
        stats[p.name] = FighterStats(
            name=p.name,
            cls_name=p.__class__.__name__,
        )
    return stats[p.name]


def fight(
    fighter_a: Person,
    fighter_b: Person,
    round_no: int,
    match_no: int,
    stats: Dict[str, FighterStats],
) -> MatchResult:
    attacker, defender = (
        (fighter_a, fighter_b)
        if random.random() < 0.5
        else (fighter_b, fighter_a)
    )

    attack_actions = 0
    resolved_by = "ko"

    if VERBOSE_FIGHT_LOG:
        print("\n__NEW fight is begin!__")
        print(f"Fighter A: {fighter_a}")
        print(f"Fighter B: {fighter_b}")

    while (
        fighter_a.hp > 0
        and fighter_b.hp > 0
        and attack_actions < MAX_ATTACK_ACTIONS_PER_MATCH
    ):
        attack_actions += 1

        raw_damage, is_crit, atk_item = calc_damage(attacker)
        total_prot, def_item = calc_protection(defender)
        hit = max(0.0, raw_damage - total_prot)

        if VERBOSE_FIGHT_LOG:
            print(f"Attacker {attacker.name} uses {atk_item}")
            if is_crit:
                print(
                    "CRIT x3! Base ATK "
                    f"{attacker.base_attack} -> "
                    f"{attacker.base_attack * 3}"
                )
            print(f"Defender {defender.name} blocks with {def_item}")
            if hit == 0.0:
                print("🛡️ Blocked! No damage this hit.")
            else:
                print(f"Hit: {hit:.1f}")

        apply_hit(defender, hit)

        s_att = get_stats(stats, attacker)
        s_def = get_stats(stats, defender)

        s_att.attacks += 1
        if is_crit:
            s_att.crits += 1
        if hit > 0:
            s_att.successful_hits += 1
        else:
            s_att.blocks += 1

        s_att.damage_dealt += hit
        s_def.damage_taken += hit
        s_att.max_single_hit = max(s_att.max_single_hit, hit)

        if VERBOSE_FIGHT_LOG:
            print(f"After hit: {defender.name} HP={defender.hp:.1f}")

        attacker, defender = defender, attacker

        if BATTLE_SPEED > 0:
            sleep(BATTLE_SPEED)

    if (
        attack_actions >= MAX_ATTACK_ACTIONS_PER_MATCH
        and fighter_a.hp > 0
        and fighter_b.hp > 0
    ):
        resolved_by = "timeout"
        if VERBOSE_FIGHT_LOG:
            print("⏱️ Match timeout reached. Resolving by current HP.")

        if fighter_a.hp > fighter_b.hp:
            winner, loser = fighter_a, fighter_b
        elif fighter_b.hp > fighter_a.hp:
            winner, loser = fighter_b, fighter_a
        else:
            winner, loser = (
                (fighter_a, fighter_b)
                if random.random() < 0.5
                else (fighter_b, fighter_a)
            )
    else:
        winner, loser = (
            (fighter_a, fighter_b)
            if fighter_a.hp > 0
            else (fighter_b, fighter_a)
        )

    s_w = get_stats(stats, winner)
    s_l = get_stats(stats, loser)
    s_w.fights += 1
    s_l.fights += 1
    s_w.wins += 1
    s_l.losses += 1

    if VERBOSE_FIGHT_LOG:
        print(
            "🏁 Winner: "
            f"{winner.name} (HP={winner.hp:.1f}) | "
            "Loser: "
            f"{loser.name} (HP={loser.hp:.1f})"
        )

    return MatchResult(
        round_no=round_no,
        match_no=match_no,
        a_name=fighter_a.name,
        b_name=fighter_b.name,
        winner=winner.name,
        loser=loser.name,
        attacks=attack_actions,
        winner_hp=winner.hp,
        loser_hp=loser.hp,
        resolved_by=resolved_by,
    )


def run_tournament(
    fighters: List[Person],
) -> Tuple[Person, List[List[MatchResult]], Dict[str, FighterStats]]:
    bracket: List[List[MatchResult]] = []
    stats: Dict[str, FighterStats] = {}

    current_round = fighters[:]
    round_no = 1

    while len(current_round) > 1:
        random.shuffle(current_round)

        next_round: List[Person] = []
        round_matches: List[MatchResult] = []
        match_no = 1

        i = 0
        while i < len(current_round):
            if i + 1 >= len(current_round):
                bye_fighter = current_round[i]
                get_stats(stats, bye_fighter)
                next_round.append(bye_fighter)

                round_matches.append(
                    MatchResult(
                        round_no=round_no,
                        match_no=match_no,
                        a_name=bye_fighter.name,
                        b_name=None,
                        winner=bye_fighter.name,
                        loser=None,
                        attacks=0,
                        winner_hp=bye_fighter.hp,
                        loser_hp=None,
                        resolved_by="bye",
                    )
                )
                match_no += 1
                i += 1
                continue

            fighter_a = current_round[i]
            fighter_b = current_round[i + 1]

            res = fight(fighter_a, fighter_b, round_no, match_no, stats)
            round_matches.append(res)

            winner_obj = (
                fighter_a if res.winner == fighter_a.name else fighter_b
            )
            next_round.append(winner_obj)

            match_no += 1
            i += 2

        bracket.append(round_matches)
        current_round = next_round
        round_no += 1

    champion = current_round[0]
    return champion, bracket, stats


def print_bracket(bracket: List[List[MatchResult]]) -> None:
    print("\n" + "=" * 28)
    print("🏟️  TOURNAMENT BRACKET")
    print("=" * 28)

    for round_matches in bracket:
        if not round_matches:
            continue

        round_no = round_matches[0].round_no
        print(f"\nRound {round_no}")

        for m in round_matches:
            if m.resolved_by == "bye":
                print(f"  [{m.match_no}] {m.a_name} gets a BYE → advances")
                continue

            print(
                f"  [{m.match_no}] {m.a_name} vs {m.b_name} → "
                f"{m.winner} ({m.resolved_by}, attacks={m.attacks}, "
                f"HP={m.winner_hp:.1f})"
            )


def print_stats(
    stats: Dict[str, FighterStats],
    bracket: List[List[MatchResult]],
) -> None:
    print("\n" + "=" * 28)
    print("📊  BATTLE STATS")
    print("=" * 28)

    top_wins = sorted(
        stats.values(),
        key=lambda s: (s.wins, s.damage_dealt),
        reverse=True,
    )[:5]
    print("\nTop wins:")
    for s in top_wins:
        print(
            f"  {s.name} ({s.cls_name}) — wins={s.wins}, "
            f"fights={s.fights}, dmg={s.damage_dealt:.1f}"
        )

    top_damage = sorted(
        stats.values(),
        key=lambda s: s.damage_dealt,
        reverse=True,
    )[:5]
    print("\nTop damage dealers:")
    for s in top_damage:
        print(
            f"  {s.name} — dmg_dealt={s.damage_dealt:.1f}, "
            f"hits={s.successful_hits}/{s.attacks}, crits={s.crits}"
        )

    top_crits = sorted(stats.values(), key=lambda s: s.crits, reverse=True)[:5]
    print("\nTop crits:")
    for s in top_crits:
        print(f"  {s.name} — crits={s.crits}")

    longest: Optional[MatchResult] = None
    for rnd in bracket:
        for m in rnd:
            if m.resolved_by == "bye":
                continue
            if longest is None or m.attacks > longest.attacks:
                longest = m

    if longest is not None:
        print("\nLongest match:")
        print(
            f"  Round {longest.round_no} Match {longest.match_no}: "
            f"{longest.a_name} vs {longest.b_name} → {longest.winner} "
            f"(attacks={longest.attacks}, resolved_by={longest.resolved_by})"
        )


def main() -> None:
    fighters = dress_up_warrior()
    print(f"Имен в списке: {len(WARRIORS_NAMES)}")

    champion, bracket, stats = run_tournament(fighters)

    print_bracket(bracket)

    print("\n" + "🏆" * 10)
    print(f"Champion: {champion}")
    print("🏆" * 10)

    print_stats(stats, bracket)


if __name__ == "__main__":
    main()
