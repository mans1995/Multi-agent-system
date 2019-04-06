#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================



#==================================================
#  AGENT
#==================================================

# ---Imports---

import math
from random import randrange, shuffle, uniform

import mas_environment as e
import mas_population as p
import mas_cell as c
import mas as m
import mas_walker as w
import mas_utils as u
import mas_utils_mod as u_mod


AGENT_MAX_IDX = 10
AGENT_METABOLISM_IDX = 0
AGENT_VISION_IDX = 1
AGENT_SUGAR_LEVEL_IDX = 2
AGENT_POSITION_IDX = 3
AGENT_AGE_IDX = 4
AGENT_DEAD_AGE_IDX = 5
AGENT_SEX_IDX = 6
AGENT_GESTATION_IDX = 7
AGENT_PARTNER_SPEC_IDX = 8
AGENT_WARRIOR_STATE_IDX = 9
AGENT_POP_IDX = 10

# ---Constants---

AGENT_MIN_VISION = 3
AGENT_MAX_VISION = 11           # (VISION BETWEEN 3 AND 10)
AGENT_MIN_METABOLISM = 0.1  
AGENT_MAX_METABOLISM = 0.2      # (METABOLISM BETWEEN 0.1 AND 0.2)
AGENT_MIN_DEAD_AGE = 20
AGENT_MAX_DEAD_AGE = 121        # (DEAD AGE BETWEEN 20 AND 120)

# ---Initialisation---

def __empty_instance():
    """
        Returns an empty agent.
    """
    return [None]*(AGENT_MAX_IDX+1)

def new_instance(pop):
    """
        Returns an initialized agent .
    """
    from random import randrange
    agent = __empty_instance()
    set_metabolism(agent, uniform(AGENT_MIN_METABOLISM, AGENT_MAX_METABOLISM))  
    set_vision(agent, randrange(AGENT_MIN_VISION, AGENT_MAX_VISION))             
    set_sugar_level(agent, 1.0)
    set_pos(agent, (-1,-1))
    set_age(agent, 0)
    set_dead_age(agent, randrange(AGENT_MIN_DEAD_AGE, AGENT_MAX_DEAD_AGE))      
    set_sex(agent, randrange(0,2))                                              # (SEX = 0 (female) or SEX = 1 (male))
    set_gestation(agent, -1)
    set_warrior_state(agent, 0)
    set_pop(agent, pop)
    return agent


def show(agent):
    """
        Shows the agent in the display console.
    """
    print( str(get_pos(agent)) + ": "\
           + "metabolism: " + str(get_metabolism(agent)) + "\t"\
           + "vision: " + str(get_vision(agent)) + "\t"\
           + "sugar level: " + str(get_sugar_level(agent)) + "\t"\
           + "age: " + str(get_age(agent)) + "\t"\
           + "dead age: " + str(get_dead_age(agent)) + "\t"\
           + "sex: " + str(get_sex(agent)) + "\t"\
           + "gestation state: " + str(get_gestation(agent)) + "\t"\
           + "warrior state: " + str(get_warrior_state(agent)) + "\t")

# ---Get/Set---

def get_pop(agent):
    """
        Returns the population (list) the agent belongs to.
    """
    return agent[AGENT_POP_IDX]

def set_pop(agent, new_pop):
    """
        Modifies the population (list)  the agent belongs to.
    """
    agent[AGENT_POP_IDX] = new_pop

def get_metabolism(agent):
    """
        Returns the metabolism (float) of the agent.
    """
    return agent[AGENT_METABOLISM_IDX]

def set_metabolism(agent, new_metabolism):
    """
        Modifies the metabolism (float) of the agent to
        a new_matabolism(float).
    """
    agent[AGENT_METABOLISM_IDX] = new_metabolism

def get_vision(agent):
    """
        Returns the vision (int) of the agent.
    """
    return agent[AGENT_VISION_IDX]

def set_vision(agent, new_vision):
    """
        Modifies the vision (int) of the agent to
        a new vision (int)
    """
    agent[AGENT_VISION_IDX] = new_vision

def get_sugar_level(agent):
    """
        Returns the sugar level (float) of the agent.
    """
    return agent[AGENT_SUGAR_LEVEL_IDX]

def set_sugar_level(agent, new_sugar_level):
    """
        Modifies the sugar level (float) of the agent to
        a new sugar_level (float)
    """
    agent[AGENT_SUGAR_LEVEL_IDX] = new_sugar_level

def get_pos(agent):
    """
        Returns the position (tuple(int, int)) of the agent.
    """
    return agent[AGENT_POSITION_IDX]

def set_pos(agent, new_pos):
    """
        Modifies the position (tuple(int, int)) of the agent to
        a new position (tuple(int, int))
    """
    agent[AGENT_POSITION_IDX] = new_pos

def get_age(agent):
    """
        Returns the age (int) of the agent.
    """
    return agent[AGENT_AGE_IDX]

def set_age(agent, new_age):
    """
        Modifies the age (int) of the agent to
        a new age (int)
    """
    agent[AGENT_AGE_IDX] = new_age


def get_dead_age(agent):
    """
        Returns the age of dead (float) of the agent.
    """
    return agent[AGENT_DEAD_AGE_IDX]

def set_dead_age(agent, new_dead_age):
    """
        Modifies the dead age (int) of the agent to
        a new dead age (int)
    """
    agent[AGENT_DEAD_AGE_IDX] = new_dead_age
    
def get_sex(agent):
    """
        Returns the sex (0 = female or 1 = male) of the agent.
    """
    return agent[AGENT_SEX_IDX]

def set_sex(agent, new_sex):
    """
        Modifies the sex (1 or 0) of the agent to
        a new sex(0 or 1)
    """
    agent[AGENT_SEX_IDX] = new_sex

def get_gestation(agent):
    """
        Returns the gestation (float) of the agent.
        If it is -1, it means there's no gestation.
        Applied to a female.
    """
    return agent[AGENT_GESTATION_IDX]

def set_gestation(agent, new_gestation):
    """
        Modifies the gestation (int) of the agent to
        a new gestation (int)
    """
    agent[AGENT_GESTATION_IDX] = new_gestation

def get_partner_spec(agent):
    """
        Returns a tuple with the dead age and the metabolism
        (tuple(int, float)) of the sexual partner of the agent.
        Applied to a female.
    """
    return agent[AGENT_PARTNER_SPEC_IDX]

def set_partner_spec(agent, new_spec):
    """
        Modifies the tuple with the dead age and the metabolism
        (tuple(int, float)) of the sexual partner of agent to
        a new tuple with the dead age and the metabolism
        (tuple(int, float))
    """
    agent[AGENT_PARTNER_SPEC_IDX] = new_spec

def get_warrior_state(agent):
    """
        Returns 1 if the agent is a warrior, 0 otherwise.
        Warriors are male agents who can kill contaminated agents.
        Applied to a male.
    """
    return agent[AGENT_WARRIOR_STATE_IDX]

def set_warrior_state(agent, new_state):
    """
        Modifies the warrior state (1 or 0) of the agent to
        a new warrior state (0 or 1)
    """
    agent[AGENT_WARRIOR_STATE_IDX] = new_state

# ---Kill---

def kill_agent(pop, agent):
    """
        Kills the agent.
    """
    env = p.get_env(pop)
    cell = e.get_cell(env, get_pos(agent))
    p.end_agent(agent, p.get_agents(pop))
    c.set_present_agent(cell, None)

# ---Eating function---

def eat_and_consumpt_sugar(agent, cell):
    """
        Adds the sugar level of the cell to the sugar level of
        the agent and makes the cell empty.
        It also reduce the agent's sugar level because of his
        metabolism.
    """
    new = get_sugar_level(agent) + c.get_sugar_level(cell)
    set_sugar_level(agent, new)
    c.set_sugar_level(cell, 0)
    new2 = get_sugar_level(agent) - get_metabolism(agent)
    set_sugar_level(agent, new2)

# --- BONUS FUNCTIONS---

def agent_is_warrior(agent):
    """
        Returns True if the agent is a warrior, False otherwise.
    """
    return get_warrior_state(agent) != 0

def add_age(agent):
    """
        Increments the age of the agent by one.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    cell = e.get_cell(env, get_pos(agent))
    age = get_age(agent)
    set_age(agent, age+1)
    if age > get_dead_age(agent):
        kill_agent(pop, agent)

def partners_list_under_conditions(env, agent, l_pos):
    """
        Returns the partner list of a female agent.
        This list must consider the conditions of age
        and sex of the agent and her partner.
    """
    l_partners = []
    for pos in l_pos:
        cell = e.get_cell(env, pos)
        partner = c.get_present_agent(cell)
        if len(partner) == AGENT_MAX_IDX +1 and get_sex(agent) == 0 and get_sex(agent) != get_sex(partner)\
           and get_age(agent) > 20 and get_age(partner) > 20 and get_sugar_level(agent) > 10\
           and get_sugar_level(partner):
            l_partners.append(partner)
    return l_partners
    
def best_partner_from_list(l_partners):
    """
        Returns the best partner of a list of partners to make the population
        evolve according to a simplified vision of the natural selection.
    """
    if len(l_partners) != 0:
        l_ages = []
        for male in l_partners:
            l_ages.append(get_dead_age(male))
        max_age = max(l_ages)
        for male in l_partners:
            if get_dead_age(male) == max_age:
                partner = male
    return partner

def reproduction(agent):
    """
        Choose the best male around the female agent in order the make her
        enter in a gestation period which will allow to give birth to a new
        agent 9 cycles after the reproduction.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    first_pop_size = len(p.get_agents(pop))
    l, l_pos = potential_partners(pop, agent, env, env_size, 1, l = [], l_pos = [])
    l_partners = partners_list_under_conditions(env, agent, l_pos)
    if len(l_partners) != 0:
        best_age = get_dead_age(best_partner_from_list(l_partners))
        metabolism = get_metabolism(best_partner_from_list(l_partners))
        if get_gestation(agent) == -1:
            set_gestation(agent, 9)
            set_partner_spec(agent, (best_age, metabolism))

def add_baby_agent_if_possible(env, pop, env_size, agent, l_pos):
    """
        Makes a female agent give birth to a new agent if there is a free
        position around her. If there is no free position, the baby won't
        born. This strategy limmits the overpopulation.
    """
    if len(l_pos) != 0:
        baby = new_instance(pop)
        mother_dead_age = get_dead_age(agent)
        mother_metabolism = get_metabolism(agent)
        father_dead_age = get_partner_spec(agent)[0]
        father_metabolism = get_partner_spec(agent)[1]
        set_dead_age(baby, int((mother_dead_age+father_dead_age)/2))
        set_metabolism(baby, (mother_metabolism+father_metabolism)/2)
        p.get_agents(pop).append(baby)
        set_pos(baby, l_pos[0])
        c.set_present_agent(e.get_cell(env, l_pos[0]), baby)

def give_birth(agent):
    """
        Makes the pregnant female agent give birth if it is her correct
        cycle or decrement her cycle by one otherwise.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    if get_gestation(agent) == 0:
        l, l_pos = potential_places(pop, agent, env, env_size, 1, l = [], l_pos = [])
        add_baby_agent_if_possible(env, pop, env_size, agent, l_pos)
    if get_gestation(agent) > -1:
        set_gestation(agent, get_gestation(agent)-1)
        if  get_sugar_level(agent) > 10/9:
            set_sugar_level(agent,  get_sugar_level(agent)-10/9)
        else:
            set_gestation(agent, -1)

def add_partner_in_places(env, env_size, l, l_pos , i, j):
    """
        Adds two different elements to two different lists. The first one is
        composed by the cells containing potential males and the second one
        contains the positions of this cells in the environment.
    """
    cell = e.get_cell(env, (i%env_size, j%env_size))
    if c.agent_is_present(cell):
        l.append(cell)
        l_pos.append((i%env_size, j%env_size))

def potential_partners(pop, agent, env, env_size, vision, l = [], l_pos = []):
    """
        Returns two lists. The first one is composed by the cells containing
        potential males and the second one contains the positions of this cells
        in the environment.
    """   
    pos_x, pos_y = get_pos(agent)
    for i in range(pos_x-vision, pos_x+vision+1):
        if i != pos_x:
            add_partner_in_places(env, env_size, l, l_pos, i, pos_y)
    for i in range(pos_y-vision, pos_y+vision+1):
        if i != pos_y:
            add_partner_in_places(env, env_size, l, l_pos, pos_x, i)
    return l, l_pos

def walker_around_check(pop, agent):
    """
        Returns the list of the contamined cells around the agent.
    """
    walker_around = False
    l_around = []
    env = p.get_env(pop)
    x, y = get_pos(agent)
    all_x = range(x-1, x+2)
    all_y = range(y-1, y+2)
    for i in all_x:
        for j in all_y:
            cell = e.get_cell(env, (i, j))
            l_around.append(c.get_present_agent(cell))
    for elem in l_around:
        if elem != None and len(elem) == w.WALKER_MAX_IDX+1:
            walker_around = True
    return walker_around


def not_immune(agent):
    """
        This agent_rule makes the agents sensible to an eventually
        contamination by the contamined cells. It doesn't affect
        the warriors agents.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    walker_around = walker_around_check(pop, agent)    
    if walker_around and not agent_is_warrior(agent):
        x, y = get_pos(agent)
        cell = e.get_cell(env, (x, y))
        if not agent_is_warrior(agent) and get_age(agent) <= 20:            # TOO YOUNG AND NOT A WARRIOR
            kill_agent(pop, agent)
        elif not agent_is_warrior(agent) and get_age(agent) > 20:           # MATURE AND NOT A WARRIOR
            kill_agent(pop, agent)
            walker = w.new_instance(pop)
            w.set_pos(walker, (x, y))
            c.set_present_agent(cell, walker)
            p.add_walker(walker, p.get_walkers(pop))

def become_warrior(agent):
    """
        Every male agent has one chance (on two) to become a warrior.
    """
    pop = get_pop(agent)
    a = randrange(2)
    if a == 0:
        if get_age(agent) == 35 and get_sex(agent) == 1:                # MALE OF 35 "YEARS"       
            set_warrior_state(agent, 1)
            set_vision(agent, min(get_vision(agent)+3, AGENT_MAX_VISION)) # BETTER VISION WHEN BECOMING SOLDIER
            

# --- Functions used by rules RA1/RA2/RA3/RA4 ---

def get_is_living(agent):
    """
        Returns True if the sugar level of the agent is bigger
        than 0, False otherwise.
    """
    alive = True
    if get_sugar_level(agent) <= 0:
        alive = False
    return alive

def add_cell_in_places(agent, env, env_size, l, l_pos , i, j):
    """
        Adds two different elements to two different lists. The first one is
        composed by the cells containing potential places and the second one
        contains the positions of this cells in the environment.
    """
    cell = e.get_cell(env, (i%env_size, j%env_size))
    if agent_is_warrior(agent) and c.get_present_agent(cell) == "alerte":
        l.append(cell)
        l_pos.append((i%env_size, j%env_size))        
    if not c.agent_is_present(cell):
        l.append(cell)
        l_pos.append((i%env_size, j%env_size))
    return l, l_pos    


def potential_places(pop, agent, env, env_size, vision, l = [], l_pos = []):  
    """
        Returns two lists. The first one is composed by the cells containing
        potential places and the second one contains the positions of this cells
        in the environment.
    """   
    pos_x, pos_y = get_pos(agent)
    for i in range(pos_x-vision, pos_x+vision+1):
        if i != pos_x:
            add_cell_in_places(agent, env, env_size, l, l_pos, i, pos_y)
    for i in range(pos_y-vision, pos_y+vision+1):
        if i != pos_y:
            add_cell_in_places(agent, env, env_size, l, l_pos, pos_x, i)
    return l, l_pos

def max_ressource_cell_position(l, l_pos):
    """
        Returns the position of the cell of the environment which has
        the biggest sugar level.
    """
    l_res = []
    for elem in l:
        l_res.append(c.get_sugar_level(elem))
    max_res =  max(l_res)
    for i in range(len(l)):
        if c.get_sugar_level(l[i]) == max_res:
            pos_cell = l_pos[i]
    return pos_cell

def best_ressource(agent, l_res, best_value):
    """
        Returns the sugar level of the cell of the environment which
        has the biggest sugar level.
    """
    for i in range(len(l_res)):
        if l_res[i] == best_value:
            agent_idx = i
    if agent_idx < len(l_res)-1:
        best_res = l_res[agent_idx+1]        
    elif agent_idx == len(l_res)-1:
        best_res = l_res[agent_idx-1]
    return best_res

def better_ressource_cell_position(l, l_pos, agent):
    """
        Returns the position of the cell in the environment which has
        enough sugar for the metabolism of the agent. But this sugar
        level must be near the metabolism of the agent (as near as possible).
        But if the metabolism of the agent is bigger than every sugar level of
        every cell, then this function returns the position of the nearest
        sugar level. Used for RA3.
    """
    l_res = []
    for elem in l:
        l_res.append(c.get_sugar_level(elem))
    l_res.append(get_metabolism(agent))
    l_res.sort()
    best_res = best_ressource(agent, l_res, get_metabolism(agent))
    for i in range(len(l)):
        if c.get_sugar_level(l[i]) == best_res:
            pos_cell = l_pos[i]
    return pos_cell

def better_ressources_for_average(l, l_pos, agent):
    """
        Returns the list of the positions of the cells which have enough
        sugar compared with the metabolism of the agent. But if the metabolism
        of the agent is bigger than every sugar level of every cell, it
        returns a list containing the cell which has the biggest sugar level.
    """
    l_res = []
    l_good_pos = []
    for elem in l:
        l_res.append(c.get_sugar_level(elem))
    u.sort_on_second_list(l_pos, l_res, u_mod.order_scalar_asc)
    if len(l_res) > 0:
        if get_metabolism(agent) > max(l_res):
            l_good_pos = [l_pos[len(l_pos)-1]]
        else:
            for i in range(len(l_res)):
                if l_res[i] > get_metabolism(agent):
                    l_good_pos.append(l_pos[i])
    return l_good_pos   

def better_average_ressource_cell(l, l_good_pos, l_average_res, agent):
    """
        Returns the position of the cell which has the closest average
        sugar level (the average of the sugar level of the agents who are
        near the cell). "Closest" means here, just above the sugar level
        of the agent.
    """
    pos_cell = get_pos(agent)
    u.sort_on_second_list(l_good_pos, l_average_res, u_mod.order_scalar_asc)
    if len(l_average_res) > 0:
        if get_sugar_level(agent) >= max(l_average_res):
            pos_cell = l_good_pos[len(l_good_pos)-1]
        else:
            possible_pos = []
            for i in range(len(l_average_res)):
                if l_average_res[i] > get_sugar_level(agent):
                    possible_pos.append(l_good_pos[i])
            pos_cell = min(possible_pos)
    return pos_cell
    
def add_average_sugar_level(tot_list, l_average_res):
    """
        Adds an average of the numbers in a list to another list.
    """
    tot = 0
    for elem in tot_list:
        tot += elem
    if len(tot_list) > 0:
        tot /= len(tot_list)
    else:
        tot = 0
    l_average_res.append(tot)

def average_around_agents_sugar_level(env, l_good_pos):
    """
        Returns a list containing list containing the average of the
        sugar level of the agents around the cells where the agent can
        go.
    """
    vision = 3
    l_average_res = []
    for pos in l_good_pos:    
        x, y = pos
        tot_list = []
        for i in range(x-vision, x+vision+1):
            for j in range(y-vision, y+vision+1):
                cell = e.get_cell(env, (i, j))
                if (i, j) != (x, y) and c.agent_is_present(cell) and len(c.get_present_agent(cell)) == AGENT_MAX_IDX+1:
                    agent = c.get_present_agent(cell)
                    tot_list.append(get_sugar_level(agent))
        add_average_sugar_level(tot_list, l_average_res)
    return l_average_res

def deplacement_into_unit(deplacement):
    """
        Returns a tuple of two int containing the pos of the next cell
        where the agent will have to go in order to reach the highest
        sugar level in his vision.
    """
    d = []
    for elem in deplacement:
        if elem < 0:
            d.append(-1)
        elif elem == 0:
            d.append(0)
        else:
            d.append(1)
    return d

def ref_adapted_to_env(env_size, vect):
    """
        Returns a tuple of two int containing a position which is in
        the env.
    """
    new_vect = []
    for elem in vect:
        new_vect.append(elem%env_size)
    return tuple(new_vect)

def deplace_or_remove(env, pop, agent, cell, pos_cell):
    """
        If the agent has enough sugar (float > 0), he can move to  his next
        position, he dies and completely disappears otherwise.
    """
    c.set_present_agent(e.get_cell(env, get_pos(agent)), None)
    if get_is_living(agent):        
        set_pos(agent, pos_cell)
        c.set_present_agent(cell, agent)
    else:
        kill_agent(pop, agent)

def possible_cell_position(env, agent, pos):
    """
        Returns a tuple of two int containing the next position of
        an agent.
    """
    if c.get_present_agent(e.get_cell(env, pos)) == "alerte" and agent_is_warrior(agent):
        pos_cell = pos
    elif not c.agent_is_present(e.get_cell(env, pos)):
        pos_cell = pos
    else:
        pos_cell = get_pos(agent)
    return pos_cell

def unital_move(env, env_size, agent, pos_cell):
    """
        Makes the movement of the agent respecting the RA2 rule which makes
        the agents move from one cell to another cell which is just one cell further.
    """
    deplacement = deplacement_into_unit(u.vector_diff(pos_cell, get_pos(agent)))
    save = ref_adapted_to_env(env_size, u.vector_sum(get_pos(agent), deplacement))
    return possible_cell_position(env, agent, save)
    
# --- Rules RA1/RA2/RA3/RA4 ---

def RA1(agent):
    """
        This first rule makes the agents move to the cell in their vision which has
        the biggest sugar level.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    l, l_pos = potential_places(pop, agent, env, env_size, get_vision(agent), l = [], l_pos = [])    
    pos_cell = get_pos(agent)
    if len(l_pos) > 0:
        pos_cell = max_ressource_cell_position(l, l_pos)
    cell = e.get_cell(env, pos_cell)
    eat_and_consumpt_sugar(agent, cell)
    deplace_or_remove(env, pop, agent, cell, pos_cell)    

def RA2(agent):
    """
        This second rule makes the agents see the cell in their vision which has
        the biggest sugar level. But they can only move one step by one step.
        It means that this cell can change at every cycle.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    l, l_pos = potential_places(pop, agent, env, env_size, get_vision(agent), l = [], l_pos = [])    
    pos_cell = get_pos(agent)
    if len(l_pos) > 0:
        pos_cell = max_ressource_cell_position(l, l_pos)
        pos_cell = unital_move(env, env_size, agent, pos_cell)
    cell = e.get_cell(env, pos_cell)
    eat_and_consumpt_sugar(agent, cell)
    deplace_or_remove(env, pop, agent, cell, pos_cell)

def RA3(agent):
    """
        This third rule makes the agents move to the cell in their vision which has
        the best sugar level. "Best" means as closest as possible to the metabolism
        of the agent. And if the sugar level of the cell is close enough and bigger
        the the metabolism of the agent, then he will move to this cell.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    l, l_pos = potential_places(pop, agent, env, env_size, get_vision(agent), l = [], l_pos = [])    
    pos_cell = get_pos(agent)
    if len(l_pos) > 0:
        pos_cell = better_ressource_cell_position(l, l_pos, agent)
    cell = e.get_cell(env, pos_cell)
    eat_and_consumpt_sugar(agent, cell)
    deplace_or_remove(env, pop, agent, cell, pos_cell)

def RA4(agent):
    """
        This fourth rule makes the agents move to the cell which has enough sugar for
        his metabolism, or to the cell which has the closest sugar level to his metabolism
        if there is no cell which has a bigger sugar level than the meatabolism of the
        agent. After this, this rule checks the average of the sugar levels of the agents
        who are near every cell the agent can move to. This agent will choose a cell which
        has this average result above the sugar level of the agent. If it is not possible, the
        agent will go on the cell with the nearest average result.
    """
    pop = get_pop(agent)
    env = p.get_env(pop)
    env_size = e.size(env)
    l, l_pos = potential_places(pop, agent, env, env_size, get_vision(agent), l = [], l_pos = [])    
    pos_cell = get_pos(agent)
    if len(l_pos) > 0:
        l_good_pos = better_ressources_for_average(l, l_pos, agent)
        l_average_res = average_around_agents_sugar_level(env, l_good_pos)
        pos_cell = better_average_ressource_cell(l, l_good_pos, l_average_res, agent)
    cell = e.get_cell(env, pos_cell)
    eat_and_consumpt_sugar(agent, cell)
    deplace_or_remove(env, pop, agent, cell, pos_cell)

# --- Deplacement orders OA1/OA2 ---

def OA1(agent):
    """
        This rule activates the agents in an random order at every cycle.
    """
    pop = get_pop(agent)
    if agent == p.get_agents(pop)[0]:                #IF IT IS THE FIRST AGENT
        shuffle(p.get_agents(pop))

def OA2(agent):
    """
        This rule activates the agents in an order which makes the agent
        who has the lowest sugar level move first. This order changes at
        every cycle.
    """
    pop = get_pop(agent) 
    if agent == p.get_agents(pop)[0]:               #IF IT IS THE FIRST AGENT
        l_res = []
        for elem in p.get_agents(pop):
            l_res.append(get_sugar_level(elem))        
        u.sort_on_second_list(p.get_agents(pop), l_res, u_mod.order_scalar_asc)
