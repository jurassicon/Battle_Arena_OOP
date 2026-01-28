import pytest

import arena


def test_apply_hit_rounds_and_never_negative():
    p = arena.Person("Bob", hp=10, attack=1, protection=0.0)

    arena.apply_hit(p, 0.04)
    assert p.hp == 10.0  # round(10 - 0.04, 1) -> 10.0

    arena.apply_hit(p, 0.05)
    assert p.hp == 9.9  # round(10.0 - 0.05, 1) -> 9.9

    arena.apply_hit(p, 999)
    assert p.hp == 0.0  # hp must not go below 0.0


def test_calc_damage_crit_and_weapon_selected(monkeypatch):
    attacker = arena.Person("Alice", hp=40, attack=10, protection=0.0)
    w = arena.Weapon("Sword", protection=0.0, damage=5)
    attacker.set_weapons([w])

    # Force selecting our weapon
    monkeypatch.setattr(arena.random, "choice", lambda seq: seq[0])
    # Force critical hit: roll_crit_multiplier() uses randint(1,10) == 1
    monkeypatch.setattr(arena.random, "randint", lambda a, b: 1)

    dmg, is_crit, selected = arena.calc_damage(attacker)

    assert selected is w
    assert is_crit is True
    # (base_attack * 3) + weapon.damage = (10*3)+5 = 35
    assert dmg == 35.0


def test_fight_timeout_resolves_by_hp(monkeypatch):
    """
    Make sure timeout branch works:
    - hit is always 0 (so nobody dies)
    - MAX_ATTACK_ACTIONS_PER_MATCH is small
    - resolve winner by higher HP at timeout
    """
    # Disable delays and logs for speed/clean output
    monkeypatch.setattr(arena, "BATTLE_SPEED", 0)
    monkeypatch.setattr(arena, "VERBOSE_FIGHT_LOG", False)
    monkeypatch.setattr(arena, "MAX_ATTACK_ACTIONS_PER_MATCH", 2)

    # Avoid actual sleeping (even if BATTLE_SPEED is mistakenly > 0 somewhere)
    monkeypatch.setattr(arena, "sleep", lambda _: None)

    # Ensure stable initial attacker selection
    monkeypatch.setattr(arena.random, "random", lambda: 0.0)

    # Setup fighters with weapons (required by calc_damage/calc_protection)
    a = arena.Person("A", hp=10, attack=1, protection=100.0)
    b = arena.Person("B", hp=20, attack=1, protection=100.0)
    w = arena.Weapon("Shield", protection=100.0, damage=0)
    a.set_weapons([w])
    b.set_weapons([w])

    # Force hit = 0 always:
    # raw_damage small, protection huge.
    monkeypatch.setattr(arena.random, "choice", lambda seq: seq[0])
    monkeypatch.setattr(arena.random, "randint", lambda a_, b_: 10)  # no crit

    stats = {}
    res = arena.fight(a, b, round_no=1, match_no=1, stats=stats)

    assert res.resolved_by == "timeout"
    assert res.winner == "B"  # B had more HP at timeout
    assert stats["B"].wins == 1
    assert stats["A"].losses == 1
