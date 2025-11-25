from dataclasses import dataclass, field

@dataclass
class EnemyStats:
    power: float
    speed: float
    damage: float
    bounty: float

@dataclass
class WeaponStats:
    power: float
    speed: float
    cooldown: float

@dataclass
class _stats:
    PLAYER_HEALTH = 20
    ENEMIES: dict[str, EnemyStats] = field(default_factory=dict)
    WEAPONS: dict[str, WeaponStats] = field(default_factory=dict)

STATS = _stats()

STATS.ENEMIES["skeleton"] = EnemyStats( power=600,     speed=2,    damage=2,   bounty=1 )
STATS.ENEMIES["orb"] =      EnemyStats( power=1200,    speed=2,    damage=1.5, bounty=2 )
STATS.ENEMIES["mage"] =     EnemyStats( power=1000,    speed=3,    damage=4,   bounty=3 )
STATS.ENEMIES["bat"] =      EnemyStats( power=100,     speed=6,    damage=0.5, bounty=0.5 )

STATS.WEAPONS["bolt"] =     WeaponStats( power=150,     speed=10,   cooldown=6 )
STATS.WEAPONS["fungus"] =   WeaponStats( power=2,       speed=4,    cooldown=40 )
STATS.WEAPONS["meteor"] =   WeaponStats( power=20,      speed=10,   cooldown=10 )
STATS.WEAPONS["star"] =     WeaponStats( power=10,      speed=10,   cooldown=0.5 )