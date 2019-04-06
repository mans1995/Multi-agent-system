#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-walker (SMA)
#
#==================================================



#==================================================
#  WALKER
#==================================================

import math
from random import randrange

import mas_environment as e
import mas_population as p
import mas_cell as c
import mas as m
import mas_agent as a
import mas_utils as u


WALKER_MAX_IDX = 2
WALKER_VISION_IDX = 0
WALKER_POSITION_IDX = 1
WALKER_POP_IDX = 2

def __empty_instance():
    """
        Returns a list with empty slots.
    """
    return [None]*(WALKER_MAX_IDX+1)

def new_instance(pop):
    """
        Initializes the walker.
    """
    walker = __empty_instance()
    set_vision(walker, 6)
    set_pos(walker, (-1, -1))
    set_pop(walker, pop)
    return walker

def show(walker):
    """
        Shows the walker into the display console.
    """
    print( str(get_pos(walker)) + ": "\
           + "vision: " + str(get_vision(walker)) + "\t")

def get_pop(walker):
    """
        Returns the population (list) the walker belongs to.
    """
    return walker[WALKER_POP_IDX]

def set_pop(walker, new_pop):
    """
        Modifies the population (list)  the walker belongs to.
    """
    walker[WALKER_POP_IDX] = new_pop

def get_vision(walker):
    """
        Returns the vision (int) of the walker.
    """
    return walker[WALKER_VISION_IDX]

def set_vision(walker, new_vision):
    """
        Modifies the vision (int) of the walker to
        a new vision (int)
    """
    walker[WALKER_VISION_IDX] = new_vision

def get_pos(walker):
    """
        Returns the position (tuple(int, int)) of the walker.
    """
    return walker[WALKER_POSITION_IDX]

def set_pos(walker, new_pos):
    """
        Modifies the position (tuple(int, int)) of the walker to
        a new position (tuple(int, int))
    """
    walker[WALKER_POSITION_IDX] = new_pos

def add_cell_in_places(env, env_size, l, l_pos , i, j):
    """
        Adds two different elements to two different lists. The first one is
        composed by the cells containing potential places and the second one
        contains the positions of this cells in the environment.
    """
    cell = e.get_cell(env, (i%env_size, j%env_size))
    if c.get_present_agent(cell) != None and len(c.get_present_agent(cell)) == a.AGENT_MAX_IDX+1:
        l.append(cell)
        l_pos.append((i%env_size, j%env_size))
    return l, l_pos

def potential_places(pop, walker, env, env_size, vision, l = [], l_pos = []):   
    """
        Returns two lists. The first one is composed by the cells containing
        potential places and the second one contains the positions of this cells
        in the environment.
    """   
    pos_x, pos_y = get_pos(walker)
    for i in range(pos_x-vision, pos_x+vision+1):
        if i != pos_x:
            add_cell_in_places(env, env_size, l, l_pos, i, pos_y)
    for i in range(pos_y-vision, pos_y+vision+1):
        if i != pos_y:
            add_cell_in_places(env, env_size, l, l_pos, pos_x, i)
    return l, l_pos

def warrior_around(l_cells_warriors):
    """
        Returns True if there is a warrior next to thr walker,
        False otherwise.
    """
    around = False
    for elem in l_cells_warriors:
        if len(c.get_present_agent(elem)) == a.AGENT_MAX_IDX+1 and a.agent_is_warrior(c.get_present_agent(elem)):
            around = True
    return around

def kill_walker(pop, walker):
    """
        Kills the walker.
    """
    env = p.get_env(pop)
    cell = e.get_cell(env, get_pos(walker))
    p.end_walker(agent, p.get_walkers(pop))
    c.set_present_agent(cell, None)
    take_aura(pop, agent)

def possible_cell_position(env, walker, pos):
    """
        Returns the position where the walker will have to go
        if there is no agent in the cell the position belongs to.
    """
    if not c.agent_is_present(e.get_cell(env, pos)) or c.get_present_agent(e.get_cell(env, pos)) == "alerte":
        pos_cell = pos
    else:
        pos_cell = get_pos(walker)
    return pos_cell

def unital_move(env, env_size, agent, pos_cell):
    """
        Makes the walkers move from one cell to another cell which is just one
        cell further.
    """
    deplacement = a.deplacement_into_unit(u.vector_diff(pos_cell, get_pos(agent)))
    save = a.ref_adapted_to_env(env_size, u.vector_sum(get_pos(agent), deplacement))
    return possible_cell_position(env, agent, save)

def unplace_walker(env, pop, walker, pos_cell):
    """
        Makes the walker and its aura disappear from the
        environment.
    """
    cell = e.get_cell(env, get_pos(walker))
    c.set_present_agent(cell, None)
    take_aura(pop, walker)
    
def replace_walker(env, pop, walker, pos_cell):
    """
        Makes the walker and its aura appear on the
        environment.
    """
    cell = e.get_cell(env, pos_cell)
    set_pos(walker, pos_cell)
    c.set_present_agent(cell, walker)
    put_aura(pop, walker)

def move_walker(mas, env, pop, walker, l_pos, env_size):
    """
        Makes the walker move to the pos_cell position.
    """
    pos_cell = get_pos(walker)
    if len(l_pos) > 0 and m.get_cycle(mas) % 2 == 0:
        pos_cell = l_pos[randrange(len(l_pos))]
        pos_cell = unital_move(env, env_size, walker, pos_cell)
    elif (len(l_pos) == 0 and m.get_cycle(mas) % 2 == 0) or (m.get_cycle(mas)% 2 == 0 and get_pos(walker) == pos_cell):
        pos_cell = try_to_move(walker, pos_cell, env, env_size)
    replace_walker(env, pop, walker, pos_cell)

def put_aura(pop, walker):
    """
        Puts the aura of the walker on the environnement.
    """
    vision = get_vision(walker)-2                                       # aura radius = vision radius -2
    env = p.get_env(pop)
    env_size = e.size(env)
    x, y = get_pos(walker)
    for i in range(x-vision, x+vision+1):
        for j in range(y-vision, y+vision+1):
            if (i, j) != (x, y):
                cell = e.get_cell(env, (i, j))
                if c.get_present_agent(cell) == None:
                    c.set_present_agent(cell, "alerte")

def take_aura(pop, walker):
    """
        Makes the aura of the walker disappear from the environnement.
    """
    vision = get_vision(walker)-1
    env = p.get_env(pop)
    env_size = e.size(env)
    x, y = get_pos(walker)
    for i in range(x-vision, x+vision+1):
        for j in range(y-vision, y+vision+1):
            if (i, j) != (x, y):
                cell = e.get_cell(env, (i, j))
                if c.get_present_agent(cell) == "alerte":
                    c.set_present_agent(cell, None)

def try_to_move(walker, pos, env, env_size):
    """
        Makes the walker move if he doesn't meet agents.
    """
    positions = [] 
    x, y = get_pos(walker)
    list_arounds = [((x+1)%env_size, y), ((x-1)%env_size, y), (x, (y+1)%env_size), (x, (y-1)%env_size)]
    for elem in list_arounds:
        cell = e.get_cell(env, elem)    
        if c.get_present_agent(cell) == None or c.get_present_agent(cell) == "alerte":
            positions.append(elem)
    if len(positions) > 0:
        pos = positions[randrange(len(positions))]
    else:
        pos = get_pos(walker)
    return pos

def deplace(walker):
    """
        Makes the walker move if it is possible and kills it if there
        is a warrior next to it.
    """
    pop = get_pop(walker)
    mas = p.get_mas(pop)
    env = p.get_env(pop)
    env_size = e.size(env)
    l, l_pos = potential_places(pop, walker, env, env_size, get_vision(walker), l = [], l_pos = [])
    pos_cell = get_pos(walker)
    unplace_walker(env, pop,walker, pos_cell)
    l_cells_warriors, l_pos_warriors = potential_places(pop, walker, env, env_size, 1, l = [], l_pos = [])
    if warrior_around(l_cells_warriors):
        p.end_walker(walker, p.get_walkers(pop))
    else:
        move_walker(mas, env, pop, walker, l_pos, env_size)
