# Battle Arena

A small console-based duel simulator with randomly generated fighters. The project is written in Python and represents an “arena” where randomly selected characters fight until one wins, using items, attack, and defense. There is a chance of a critical hit and a final “battle of winners”.

## Features
- Fighter generation with different classes: `Paladin` and `Warrior`.
- Random assignment of items (`Weapon`) to fighters with bonuses to damage and defense.
- Turn-based duels with battle logs printed to the console.
- Critical hit chance (x3 attack when health is low).
- Tournament logic: winners are collected and then fight in a final winners bracket.

## Project Structure

```
arena.py #   main executable file containing the battle logic
README.md #  this project description
.gitignore # Git ignore settings
```

## Requirements
- Python 3.8+ (3.10 or newer is recommended)

Only the standard library is used; no external dependencies are required.

## Installation & Run
1. Clone the repository or download the source code.
2. Run the simulator:
   ```bash
   python3 arena.py


Battle logs will be printed to the console. To stop the program, press Ctrl+C.

Battle logs will be printed to the console. To stop the program, press `Ctrl+C`.

## How It Works (Briefly)
- `Weapon` — an item with fields: `name`, `protection`, `damage`.
- `Person` — the base fighter class: name, health (`hp`), base attack, and base defense.
  - The `crit_chance()` method, when `hp <= 50`, gives a 10% chance to activate a critical hit (x3 attack).
- `Paladin(Person)` — more health and defense (x2).
- `Warrior(Person)` — higher base attack (x2).
- Before the fight, each fighter receives 1 to 4 random items.
- In each round, random items are chosen for attacking and defending, damage and defense are recalculated, and the fight continues until one fighter reaches `hp <= 0`.
- Winners are collected into a list and fight each other at the end.

## Customization
- Fighter names: `WARRIORS_NAMES` list in `arena.py` (top of the file).
- Items set: `THINGS` list in `arena.py`.
- Generation ranges (damage/defense/health): `generate_weapons()` and `generate_person()` functions.
- Battle speed: the `BATTLE_SPEED` delay inside the main fight loop — increase/decrease as needed.

## Known Behaviors
- Damage/defense values are calculated randomly before each hit, making fights unpredictable.
- Pair selection uses random indices and list removal, which makes every run unique.
- Output includes emojis and English phrases; you can localize the strings in `arena.py` if desired.

## Ideas for Improvements
- Add CLI parameters: number of items, hit delay, number of fighters, logging level.
- Visualize the tournament bracket and battle stats.
- Write tests for data generation and correctness of damage/defense calculations.
- Introduce balancing coefficients for classes and items.
- Save/load battle results to JSON/CSV.


---
