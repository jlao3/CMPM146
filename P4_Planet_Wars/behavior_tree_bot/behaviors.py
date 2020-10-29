import sys
from math import inf
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_or_defend(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    for enemy_fleet in state.enemy_fleets():
        if state.planets[enemy_fleet.destination_planet].owner == 1: # If it belongs to us
            defend_distance = state.distance(strongest_planet.ID, state.planets[enemy_fleet.destination_planet].ID) # Distance from our strongest planet to our sieged planet

            best_attack = inf
            attackShips = state.planets[enemy_fleet.source_planet].num_ships
            attack_planet = state.planets[enemy_fleet.source_planet]

            for enemy_planet in state.enemy_planets(): # Checking all current enemy planets
               attack_distance = state.distance(strongest_planet.ID, enemy_planet.ID) # Distance from our strongest planet to current target planet
               if attack_distance < best_attack:    # If distance from current target is less than our current best, check if we're stronger
                   required_ships = enemy_planet.num_ships + attack_distance * enemy_planet.growth_rate + 1
                   if required_ships < strongest_planet.num_ships: # If our current planet has enough required ships to take over their planet
                       best_attack = attack_distance # Best attacking distance is new target
                       attackShips = required_ships # amount required to take over
                       attack_planet = enemy_planet # Planet to take over

            for my_fleet in state.my_fleets():
                if enemy_fleet.destination_planet == my_fleet.destination_planet: # If we already have a fleet defending our planet
                    return issue_order(state, strongest_planet.ID, attack_planet.ID, attackShips) # Then attack

            if defend_distance < best_attack: # If not then judge distance,
                return issue_order(state, strongest_planet.ID, state.planets[enemy_fleet.destination_planet].ID, enemy_fleet.num_ships + 1) # Defending is closer, thus defend
            else:
                return issue_order(state, strongest_planet.ID, attack_planet.ID, attackShips) # Attacking is closer, thus attack
    return False


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)
