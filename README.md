# Multi-agent system

You can launch it using [mas_sim.py](mas_sim.py).

This system simulates agents trying to survive by eating in an environment divided in squares where:
- darker cases contain more food than lighter ones.
- blank squares contain no food.

Each agent is a disk in one square at a fixed moment in time. Here are the characteristics these agents:
- light blue/dark blue colors represent male agents.
- yellow/orange/red colors represent female agents.
- black agents are agents that kill the others (except other black agents).
- green agents are warriors able to destroy killers.
- purple agents are pregnant agents.
- the size of an agent represent its age.
- agents need to reach a certain age to be able to reproduce.

The [configuration file](test.cfg) contains rules about the agents and the environment. Most of them are self-explanatory excepted the following rules:
- OA1 : this rule activates the agents in an random order at every cycle.
- OA2 : this rule activates the agents in an order which makes the agent who has the lowest food level move first. This order changes at every cycle.
- RA1 : this first rule makes the agents move to the cell in their vision which has the biggest food level.
- RA2 : this second rule makes the agents see the cell in their vision which has the biggest food level. But they can only move one step by one step.
- RA3 : this third rule makes the agents move to the cell in their vision which has the best food level. "Best" means as closest as possible to the metabolism of the agent. And if the food level of the cell is close enough and bigger than the metabolism of the agent, then it will move to this cell.
- RA4 : this fourth rule makes the agents move to the cell which has enough food for his metabolism, or to the cell which has the closest food level to his metabolism if there is no cell which has a bigger food level than the meatabolism of the agent. After this, this rule checks the average of the food levels of the agents who are near every cell the agent can move to. This agent will choose a cell which has this average result above the food level of the agent. If it is not possible, the agent will go on the cell with the nearest average result.

Note : use the `#` symbol in the [configuration file](test.cfg) is used to avoid using a rule during the simulation.
