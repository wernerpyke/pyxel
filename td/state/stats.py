from dataclasses import dataclass

from pyke_pyxel import log_debug

@dataclass
class EnemyStats:
    power: float
    speed: float
    damage: float
    bounty: float

class WeaponPowerUp:
    def __init__(self, weapon_type: str, type: str, value: float) -> None:
        self.weapon_type = weapon_type
        self.type = type
        self.value = value
        self.count = 0
        self.increases = True

        if type == "cost" or type == "cooldown":
            self.increases = False
        elif type == "power" or type == "speed":
            self.increases = True
        else:
            raise ValueError(f"WeaponPowerUp invalid affects:{type}")
        
    def __eq__(self, other: object) -> bool:
        return isinstance(other, WeaponPowerUp) and self.type == other.type and self.weapon_type == other.weapon_type

class WeaponStats:
    def __init__(self, cost: float, power: float, speed: float, cooldown: float) -> None:
        self._cost = cost
        self._power = power
        self._speed = speed
        self._cooldown = cooldown

        self._weapon_type = ""

        self._power_ups: list[WeaponPowerUp] = []

    @property
    def cost(self) -> float:
        up = sum([(p.value * p.count) for p in self._power_ups if p.type == "cost"])
        return self._cost - (self._cost * up)
    
    @property
    def power(self) -> float:
        up = sum([(p.value * p.count) for p in self._power_ups if p.type == "power"])
        return self._power + (self._power * up)
    
    @property
    def speed(self) -> float:
        up = sum([(p.value * p.count) for p in self._power_ups if p.type == "speed"])
        return self._speed + (self._speed * up)

    @property
    def cooldown(self) -> float:
        up = sum([(p.value * p.count) for p in self._power_ups if p.type == "cooldown"])
        return self._cooldown - (self._cooldown * up)

    def _add_power_up(self, affects: str, value: float):
        up = WeaponPowerUp(self._weapon_type, affects, value)
        self._power_ups.append(up)

    def increment_power_up(self, affects: str):
        for p in self._power_ups:
            if p.type == affects:
                p.count += 1
                return
        raise ValueError(f"WeaponStats.increment_power_up invalid affects:{affects}")

class _stats:    
    def __init__(self):
        self._player_health = 10
        self._enemies: dict[str, EnemyStats] = {}
        self._weapons: dict[str, WeaponStats] = {}

    def enemy_stats(self, type: str) -> EnemyStats|None:
        return self._enemies.get(type)
    
    def weapon_stats(self, type: str) -> WeaponStats|None:
        return self._weapons.get(type)

    def weapon_cost(self, type: str) -> float:
        weapon = self._weapons.get(type)
        return weapon.cost if weapon else 99
    
    def weapon_power_ups(self, type: str) -> list[WeaponPowerUp]:
        weapon = self._weapons.get(type)
        if weapon:
            return weapon._power_ups
        else: 
            raise ValueError(f"WeaponStats.weapon_power_ups invalid type:{type}")
        
    def increment_weapon_power_up(self, type: str, affects: str):
        log_debug(f"STATS.increment_weapon_power_up {type} {affects}")
        weapon = self._weapons.get(type)
        if weapon:
            weapon.increment_power_up(affects)
        else:
            raise ValueError(f"WeaponStats.increment_weapon_power_up invalid type:{type}")

    @property
    def player_health(self) -> float:
        return self._player_health
    
    def _set_enemy_stats(self, type: str, power: float, speed: float, damage: float, bounty: float) -> EnemyStats:
        stats = EnemyStats(power, speed, damage, bounty)
        self._enemies[type] = stats
        return stats

    def _set_weapon_stats(self, type: str, cost: float, power: float,   speed: float,  cooldown: float) -> WeaponStats:
        stats = WeaponStats(cost, power, speed, cooldown)
        stats._weapon_type = type
        self._weapons[type] = stats
        return stats


STATS = _stats()

STATS._set_enemy_stats("skeleton",          power=600,      speed=2,    damage=2,   bounty=1 )
STATS._set_enemy_stats("orb",               power=1200,     speed=2,    damage=1.5, bounty=2 )
STATS._set_enemy_stats("mage",              power=1000,     speed=3,    damage=4,   bounty=3 )
STATS._set_enemy_stats("bat",               power=100,      speed=6,    damage=0.5, bounty=0.5 )

bolt = STATS._set_weapon_stats("bolt",      cost=3,         power=150,   speed=10,  cooldown=6 )
bolt._add_power_up("cooldown", 0.2)
bolt._add_power_up("power", 0.2)

fungus = STATS._set_weapon_stats("fungus",  cost=6,         power=2,     speed=4,   cooldown=40 )
fungus._add_power_up("power", 0.2)
fungus._add_power_up("speed", 0.2)

meteor = STATS._set_weapon_stats("meteor",  cost=4,         power=20,    speed=10,  cooldown=10 )
meteor._add_power_up("power", 0.2)
# TODO add a power-up type:'duration'

star = STATS._set_weapon_stats("star",      cost=2,         power=15,    speed=10,  cooldown=0.6 )
star._add_power_up("power", 0.2)
star._add_power_up("cooldown", 0.2)
# TODO add power-up type:'accuracy'