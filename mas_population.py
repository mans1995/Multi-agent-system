#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

from random import randrange
import mas_agent as a
import mas as m
import mas_environment as e
import mas_cell as c
import mas_walker as w

#==================================================
#  AGENT POPULATION
#==================================================

POP_MAX_IDX = 3
ENV_IDX = 0
POP_IDX = 1
WALKERS_IDX = 2
MAS_IDX = 3

# --- Initialisation ---

def __empty_instance():
    return [None]*(POP_MAX_IDX+1)

def new_instance(mas, sz, nb):
    """ 
        Return a new population instance of size "sz", with a number
        "nb" of conaminated cells and "declare" to which MAS it belongs to.
    """    
    pop = __empty_instance()
    set_env(pop, m.get_env(mas))
    set_agents(pop, [])
    set_walkers(pop, [])
    set_mas(pop, mas)
    for i in range(sz):
        agent = a.new_instance(pop)
        add_agent(agent, get_agents(pop))
    for i in range(nb):
        walker = w.new_instance(pop)
        add_walker(walker, get_walkers(pop))
    place_first_walkers(pop)# WALKERS FIRST
    place_first_agents(pop)
    return pop

def show(pop):
    """
        Shows the population on the display console.
    """
    print("\nAGENTS :\n")
    for elem in get_agents(pop):
        a.show(elem)
    print("\nWALKERS :\n")
    for elem in get_walkers(pop):
        w.show(elem)
    print("\n\n")

def get_mas(pop):
    """
        Returns the mas the population belongs to.
    """
    return pop[MAS_IDX]

def set_mas(pop, new_mas):
    """
        Changes the mas the population belongs to.
    """
    pop[MAS_IDX] = new_mas

def get_env(pop):
    """
        Returns the environment of the mas the population belongs to.
    """
    return pop[ENV_IDX]

def set_env(pop, new_env):
    """
        Changes the environment of the mas the population belongs to.
    """
    pop[ENV_IDX] = new_env

def get_agents(pop):
    """
        Returns the list of the agents of the population.
    """
    return pop[POP_IDX]

def set_agents(pop, new_agents):
    """
        Changes the list of the agents of the population.
    """
    pop[POP_IDX] = new_agents

def get_walkers(pop):
    """
        Returns the list of the walkers of the population.
    """
    return pop[WALKERS_IDX]

def set_walkers(pop, new_walkers):
    """
        Changes the list of the walkers of the population.
    """
    pop[WALKERS_IDX] = new_walkers

def add_agent(agent, pop):
    """
        Adds an agent into the list of the agents of the population.
    """
    pop.append(agent)

def end_agent(agent, pop):
    """
        Removes an agent into the list of the agents of the population.
    """
    pop.remove(agent)

def add_walker(walker, pop):
    """
        Adds an walker into the list of the walkers of the population.
    """
    pop.append(walker)

def end_walker(walker, pop):
    """
        Removes an agent into the list of the walkers of the population.
    """
    pop.remove(walker)

def apply_rule(pop, agent_rule):
    """
        Applies a rule of the agents to an agent.
    """
    for agent in get_agents(pop):
        agent_rule(agent)

def apply_rule_walkers(pop, walker_rule):
    """
        Applies a rule of the walkers to a walker.
    """
    for walker in get_walkers(pop):
        walker_rule(walker)

def new_first_pos(env, env_size, pop_size):
    """
        Generates a list containing tuples of 2D positions
        which are all in the same environment and at a different
        place.
    """
    first_pos = []
    for i in range(pop_size):
        x, y = randrange(env_size),randrange(env_size)
        cell = e.get_cell(env, (x, y))
        while (x, y) in first_pos and c.agent_is_present(cell):
            x, y = randrange(env_size),randrange(env_size)
            cell = e.get_cell(env, (x, y))
        else:
            first_pos.append((x,y))
    return first_pos

def place_first_agents(pop):
    """
        Places the agents when the mas begins at the places
        generated by the function new_first_pos
    """
    env = get_env(pop)
    env_size = e.size(env)
    pop_size = len(get_agents(pop))
    first_pos = new_first_pos(env, env_size, pop_size)
    for i in range(len(get_agents(pop))):
        a.set_pos(get_agents(pop)[i], first_pos[i])
        c.set_present_agent(e.get_cell(env, first_pos[i]), get_agents(pop)[i])

def place_first_walkers(pop):    
    """
        Places the walkers when the mas begins at the places
        generated by the function new_first_pos
    """
    env = get_env(pop)
    env_size = e.size(env)
    walkers_size = len(get_walkers(pop))
    first_pos = new_first_pos(env, env_size,walkers_size)
    for i in range(len(get_walkers(pop))):
        w.set_pos(get_walkers(pop)[i], first_pos[i])
        c.set_present_agent(e.get_cell(env, first_pos[i]), get_walkers(pop)[i])
        w.put_aura(pop, get_walkers(pop)[i])

