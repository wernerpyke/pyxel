from dataclasses import dataclass, field

@dataclass
class _estats:
    power: float
    speed: float
    damage: float
    bounty: float

@dataclass
class _stats:
    PLAYER_HEALTH = 20
    ENEMIES: dict[str, _estats] = field(default_factory=dict)

STATS = _stats()

STATS.ENEMIES["skeleton"] = _estats(
    power=600,
    speed=2,
    damage=2,
    bounty=1
)

STATS.ENEMIES["orb"] = _estats(
    power=1200,
    speed=2,
    damage=1.5,
    bounty=2
)

STATS.ENEMIES["mage"] = _estats(
    power=1000,
    speed=3,
    damage=4,
    bounty=3
)

STATS.ENEMIES["bat"] = _estats(
    power=100,
    speed=6,
    damage=0.5,
    bounty=0.5
)
