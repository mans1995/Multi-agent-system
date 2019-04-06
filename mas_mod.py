#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

# ALL THESE FUNCTIONS ARE REPOSTED HERE BECAUSE MAS_MOD CHANGES
# THE STRUCTURE OF THE MAS BY ADDING NEW FEATURES (MAS_WALKER)


import math
import random

import mas as m 
import mas_environment as e
import mas_cell as c
import mas_population as p
import mas_agent as a
import mas_utils as u
import mas_utils_mod as u_mod
import mas_walker as w



#==================================================
#  MAS
#==================================================

# --- Constants ---

MAX_IDX=7
ENV_IDX = 0                           # Environment
POP_IDX = 1                           # Agent population
CELL_RULES_IDX = 2                    # List of rules applied on cells
AGENT_RULES_IDX = 3                   # List of rules applied on agents
EXPERIMENT_ENDING_CONDITION_IDX = 4   # Function with the ending condition
MAX_CYCLE_IDX = 5                     # Max number of cycles per experiment
CYCLE_IDX = 6                         # Current cycle of an experiment
WALKER_RULES_IDX = 7




# --- Private functions --- 

# Note: These functions should not be called outside this module.

def __get_property(mas, property_idx):
	#  Return the value of the given property of the MAS.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid MAS property index.")
    return mas[property_idx]

def __set_property(mas, property_idx, value):
	# Set the value of the given property of the MAS.
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid MAS property index.")    
    mas[property_idx] = value

def __empty_instance():
	# Return an empty MAS instance.
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_walker_rules(mas):
	"""
        Return the walker rules of the MAS as a list of functions.
    """
	return __get_property(mas, WALKER_RULES_IDX)

def set_walker_rules(mas, rules_list):
	"""
        Set the walker rules of the MAS as a list of functions.
    """
	__set_property(mas, WALKER_RULES_IDX, rules_list)

# --- Initialisation ---

def new_instance():
	""" 
        Return a new MAS instance.
    """
	mas = __empty_instance()
	m.set_env(mas, None)
	m.set_pop(mas, None)
	m.set_cell_rules(mas, [])
	m.set_agent_rules(mas, [])
	set_walker_rules(mas, [])
	m.set_ending_condition(mas, m.DEFAULT_ENDING_CONDITION)
	m.set_max_cycle(mas, 0)
	m.set_cycle(mas, 0)
	return mas

def new_instance_from_config(config):
	""" 
        Return a new MAS instance that has been initialised according
        to the parameters passed by the configuration.
    """
	mas = new_instance()
	# Environment
	env = e.new_instance(mas, u.cfg_env_size(config))
	m.set_env(mas, env)
	env_capacity_distribs = u.cfg_capacity_distributions(config)
	for distrib in env_capacity_distribs:
	    e.add_capacity_from_string(env,distrib)
	# Agent population
	pop = p.new_instance(mas, u.cfg_pop_size(config), u_mod.cfg_walkers_number(config))
	m.set_pop(mas, pop)
	# Cell rules
	cell_rules = u.cfg_cell_rules(config)
	for rule in cell_rules:
	    m.add_cell_rule_from_string(mas,rule)
	# Agent rules
	agent_rules = u.cfg_agent_rules(config)
	for rule in agent_rules:
	    m.add_agent_rule_from_string(mas,rule)
	# Walker rules
	walker_rules = u_mod.cfg_walker_rules(config)
	for rule in walker_rules:
	    add_walker_rule_from_string(mas,rule)
	# Experiment settings
	m.set_max_cycle(mas,u.cfg_max_cycle(config))
	return mas

# --- Walker rules ---

def add_walker_rule(mas, walker_rule):
	"""
		Add a walker rule to the MAS.
	"""
	mas[WALKER_RULES_IDX].append(walker_rule)

def add_walker_rule_from_string(mas, walker_rule_str):
	"""
		Add a walker rule to the MAS based on a string
		that represents the function call.
	"""
	add_walker_rule(mas, eval("w."+walker_rule_str))

def apply_walker_rules(mas):
	"""
		Apply all walker rules to each walker of the MAS's population.
	"""
	pop = m.get_pop(mas)
	for walker_rule in get_walker_rules(mas):
		p.apply_rule_walkers(pop, walker_rule)

# --- Execution ---

def run_one_cycle(mas):
	"""
		Run one experiment cycle of the MAS.
	"""
	m.apply_cell_rules(mas)
	m.apply_agent_rules(mas)
	apply_walker_rules(mas)
