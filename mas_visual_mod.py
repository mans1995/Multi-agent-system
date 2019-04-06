#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#  ---------------------------------------------
#   Many thanks to Robert Vanden Eynde for 
#   providing this part of the code!
#  ---------------------------------------------
#
#==================================================


import mas_visual as v
import mas as m
import mas_mod as m_mod
import mas_environment as e
import mas_cell as c
import mas_population as p
import mas_agent as a
import mas_walker as w
import mas_visual as v

import tkinter as tk



#==================================================
#  VISUALISATION
#==================================================

# --- Private functions --- 

# Note: These functions should not be called outside this module.

def rgb_to_hex(rgb):
    # THIS FUNCTION CONVERTS RGB COLORS CODE INTO HEX COLORS CODE WHICH MAKES THE COLOR ATTRIBUTION EASIER
    # IT HAS BEEN FOUND ON A WEBSITE. WE DON'T OWN THIS FUNCTION.
    return '#%02x%02x%02x' % rgb

def __compute_cell_color(cell):
    # Compute the color of the cell, depending on its sugar level
    sugar_level = c.get_sugar_level(cell)
    env = c.get_env(cell)
    max_capacity = e.get_max_capacity(env)
    ratio = sugar_level / max_capacity
    color_level = int(255 * (1 - ratio))
    # convert the color level to hexadecimal representation
    hex_color_level = hex(color_level)[2:].zfill(2)
    #color_code = '#' + 'ff' + 'ff' + hex_color_level
    color_code = rgb_to_hex((color_level, color_level, color_level))     # ORIGINAL ONE
    #color_code = rgb_to_hex((160, color_level, 120))                    # OTHER ONE
    return color_code

def __draw_env(canvas, env, cell_size):
    # Draw the environment on the canvas
    env_size = e.size(env)
    for cell_ref in e.get_cell_refs(env):
        cell = e.get_cell(env, cell_ref)
        cell_ref =v.__swap_y(env_size, cell_ref)
        canvas.create_rectangle(v.__bbox_for_cell_ref(cell_ref, cell_size), fill=__compute_cell_color(cell), outline='#dddddd')

def thk(agent):
    # The thickness of the agent depends on his age
    thickness = 0.6
    if a.get_age(agent) < 35:
        thickness = 0.6*a.get_age(agent)/35
    if thickness < 0.2:
        thickness = 0.2
    return thickness

def color_agent(agent):
    """
        Changes the color of the agent depending on his state:
            little to big : depending on the age
            different levels of color : more colored, more sugar !
            all blue colors : male agent
            yellow, orange, red : female agent
            all purple colors : pregnant female agent
            all green colors : warrior male agent
            black : contaminated agent
    """
    if a.get_sugar_level(agent) <= 100:
        if a.get_sex(agent) == 0:
            if a.get_gestation(agent) == -1:
                color = rgb_to_hex((255,255-int(a.get_sugar_level(agent)/100*255),0))
            else:
                color = rgb_to_hex((146,int(a.get_sugar_level(agent)/100*255/2),146))
        elif a.get_sex(agent) == 1:
            if a.get_warrior_state(agent) == 0:
                color = rgb_to_hex((0,255-int(a.get_sugar_level(agent)/100*255),255))
            else:
                color = rgb_to_hex((0,(255-int(a.get_sugar_level(agent)/100*255/2)),0))
    else:
        if a.get_sex(agent) == 0:
            if a.get_gestation(agent) == -1:
                color = rgb_to_hex((255,0,0))
            else:
                color = rgb_to_hex((163,73,164))
        elif a.get_sex(agent) == 1:
            if a.get_warrior_state(agent) == 0:
                color = rgb_to_hex((0,0,255))
            else:
                color = rgb_to_hex((0,127,0))
    return color
        
def __draw_pop(canvas, pop, cell_size):
    # Draw the population on the canvas
    # WE ADD THE color_agent FUNCTION IN PLACE OF "red"
    # AND THE THICKNESS EVOLVES THANKS THE thk FUNCTION
    env = p.get_env(pop)
    env_size = e.size(env)
    for agent in p.get_agents(pop):
        if a.get_is_living(agent):
            cell_ref = v.__swap_y(env_size, a.get_pos(agent))
            canvas.create_oval(v.__bbox_for_cell_ref(cell_ref, cell_size, thk(agent)), fill=color_agent(agent), width=0)

def __draw_walkers(canvas, pop, cell_size):
    # Draw the walker population on the canvas
    env = p.get_env(pop)
    env_size = e.size(env)
    for walker in p.get_walkers(pop):
        cell_ref = v.__swap_y(env_size, w.get_pos(walker))            
        canvas.create_oval(v.__bbox_for_cell_ref(cell_ref, cell_size, 0.6), fill=rgb_to_hex((0,0,0)), width=0)

def __draw_mas(canvas, mas, cell_size):
    # Draw the MAS on the canvas
    env = m.get_env(mas)
    pop = m.get_pop(mas)
    if env is not None: 
        __draw_env(canvas, env, cell_size)
        # Only consider plotting the population if there is an environment
        if pop is not None:
            __draw_pop(canvas, pop, cell_size)
            __draw_walkers(canvas, pop, cell_size)

def run_experiment(mas, window_size=600):
    """
        Run an experiment on the initialised MAS with
        an animated graphical representation.
    """
    # THIS FUNCTION HAS BEEN PUT HERE BECAUSE IT USES THE M_MOD IMPORT
    # Initialise the graphical environment (tkinter)
    app = tk.Tk()
    app.geometry(str(window_size-v.TEXT_HEIGHT) + 'x' + str(window_size))
    canvas = tk.Canvas(app, width=window_size-v.TEXT_HEIGHT, height=window_size)
    canvas.pack()
    cell_size = (window_size - 2*v.MARGIN - v.TEXT_HEIGHT) / e.size(m.get_env(mas))
    # Define a local function that represents the "graphical loop"
    def tki_experiment_loop(mas):
        cycle = m.get_cycle(mas)
        canvas.delete(tk.ALL) # Clear the canvas
        __draw_mas(canvas, mas, cell_size)
        pop = m.get_pop(mas)
        canvas.create_text(v.MARGIN, v.MARGIN, anchor=tk.NW, text="Cycle #" + str(cycle))
        if not ending_condition(mas):
            m.increment_cycle(mas)
            m_mod.run_one_cycle(mas)
            app.update()
            app.after(v.TIME_OF_FRAME, tki_experiment_loop, mas)
    # Initialise the experiment (the MAS)
    m.set_cycle(mas, 0)
    ending_condition = m.get_ending_condition(mas)
    # Run the experiment
    tki_experiment_loop(mas)
    app.mainloop()
