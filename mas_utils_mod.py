#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================



import math

import mas as m
import mas_environment as e
import mas_cell as c
import mas_agent as p
import mas_walker as w
import mas_utils as u


#==================================================
#  Help functions
#==================================================

# CORRECTED VERSION. THE INITIAL ONE IN MAS_UTILS CONTAINS AN ERROR.
def order_scalar_asc(val1, val2):
    """
        Ascending ordering function on scalar values to be
        used with sorting functions.
    """
    return val1 > val2

#==================================================
#  Configuration (from a file)
#==================================================

# ALL THE FOLLOWING FUNCTIONS HAS BEEN ADDED TO LET THE USER CHANGE
# SOME PARAMETERS IN LINK WITH THE WALKERS.
def config_get_property(config, property):
    """
        Return the property from the configuration (as a string).
    """
	# If the property does not exist, return None.
    return config.get(property,None)

def cfg_walkers_number(config):
    """
        Return the walkers size from the configuration.
    """
    return int(config_get_property(config, "WALKERS_NUMBER"))

def cfg_walker_rules(config):
    """
        Return the list of walker rules from the configuration.
    """
    res = config_get_property(config,"ADD_WALKER_RULE")
    res = u.into_list(res)
    return res
