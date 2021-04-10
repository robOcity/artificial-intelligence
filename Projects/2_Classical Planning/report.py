# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Effect of Heuristic on Search Efficiency
#
# In this project, I will show you how to find solve planning problems -- Think logistics and scheduling -- using search and logic to find tractable solutions.  Classic planning problems can solve problem were the rules are known and clear cut, in other words they are _deterministic_.  Where to effects of an action are known to all, in AI, this is known as being _observable_.  In controlled environments, where change only occurs through the actions taken by a planning agent, these systmes work well.
#
# Acting in these worlds can be modeled logically.  Before an action can take place, all its necessary preconditions must first be met.  And once completed, its effects known.  Imagine you are in charge of logistics at Fed Ex, and need to find solutions for getting packages from place to place.  Flying packages long distances is common.  How would that work?  To model the action of flying a package we can use a PDDL [add link here].
#
# ```
# Action(Fly, (plane, from, to)
#     Precondition: At(plane, from) and Plane(from) and Airport(from) and Airport(to)
#     Effect: not At(plane, from) and At(plane, to)
# )
# ```
#
# Propositional logic describe the action succinctly and can be tailored to specific problems.  Knowing that we have a starting state, and goal state, a set of actions and costs associate with each action, allows us to apply search algorithms to find solutions.
# *

# %%
import pandas as pd
import numpy as np
from dataclasses import make_dataclass


# %%
Record = make_dataclass(
    "Record",
    [
        ("Problem", str),
        ("Algorithm", str),
        ("Alg_Name", str),
        ("Heuristic", str),
        ("Actions", int),
        ("Expansions", int),
        ("Goal_Tests", int),
        ("New_Nodes", int),
        ("Length", int),
        ("Time", float),
    ],
)


# %%
dataset = [
    Record("1", "1", "BFS", "", 20, 43, 56, 178, 6, 0.0284),
    Record("1", "2", "DFS", "", 20, 21, 22, 84, 20, 0.0073),
    Record("2", "1", "BFS", "", 72, 3343, 4609, 30503, 9, 0.3459),
    Record("2", "2", "DFS", "", 72, 624, 625, 5602, 619, 0.4810),
    Record("4", "4", "Greedy", "h_unmet_goals", 104, 29, 31, 280, 18, 0.0612),
    Record(
        "4",
        "11",
        "Greedy",
        "h_pg_setlevel",
        104,
        79863,
        79865,
        768641,
        14,
        30733.3346,
    ),
    Record(
        "3",
        "11",
        "Greedy",
        "h_pg_setlevel",
        88,
        12872,
        12874,
        115220,
        12,
        3046.3672,
    ),
    Record("1", "3", "UCS", "", 20, 60, 62, 240, 6, 0.0379),
    Record("1", "4", "Greedy", "h_unmet_goals", 20, 7, 9, 29, 6, 0.0032),
    Record("1", "5", "Greedy", "h_pg_levelsum", 20, 6, 8, 28, 6, 0.4590),
    Record("1", "6", "Greedy", "h_pg_maxlevel", 20, 6, 8, 24, 6, 0.1218),
    Record("1", "7", "Greedy", "h_pg_setlevel", 20, 13, 15, 53, 6, 1.2660),
    Record("1", "8", "A*", "h_unmet_goals", 20, 50, 52, 206, 6, 0.0216),
    Record("1", "9", "A*", "h_pg_levelsum", 20, 28, 30, 122, 6, 0.2154),
    Record("1", "10", "A*", "h_pg_maxlevel", 20, 43, 45, 180, 6, 0.1616),
    Record("1", "11", "A*", "h_pg_setlevel", 20, 46, 48, 192, 6, 0.7168),
    Record("2", "3", "UCS", "", 72, 5154, 5156, 46618, 9, 0.7450),
    Record("2", "4", "Greedy", "h_unmet_goals", 72, 17, 19, 170, 9, 0.0205),
    Record("2", "5", "Greedy", "h_pg_levelsum", 72, 9, 11, 86, 9, 0.4228),
    Record("2", "6", "Greedy", "h_pg_maxlevel", 72, 27, 29, 249, 9, 0.6970),
    Record(
        "2", "7", "Greedy", "h_pg_setlevel", 72, 304, 306, 2846, 10, 54.8001
    ),
    Record("2", "8", "A*", "h_unmet_goal", 72, 2467, 2469, 22522, 9, 0.7026),
    Record("2", "9", "A*", "h_pg_levelsum", 72, 357, 359, 3426, 9, 10.3350),
    Record("2", "10", "A*", "h_pg_maxlevel", 72, 2887, 2889, 26594, 9, 59.0657),
    Record(
        "2", "11", "A*", "h_pg_setlevel", 72, 2879, 2881, 26622, 9, 577.1144
    ),
    Record("3", "4", "Greedy", "h_unmet_goals", 88, 25, 27, 230, 15, 0.0519),
    Record("3", "6", "Greedy", "h_pg_maxlevel", 88, 21, 23, 195, 13, 1.8522),
    Record("4", "4", "Greedy", "h_unmet_goals", 104, 29, 31, 280, 18, 0.0615),
    Record("4", "6", "Greedy", "h_pg_maxlevel", 104, 56, 58, 580, 17, 3.6040),
    Record("3", "8", "A*", "h_unmet_goal", 88, 7388, 7390, 65711, 12, 1.2993),
    Record(
        "3", "10", "A*", "h_pg_maxlevel", 88, 9580, 9582, 86312, 12, 331.0158
    ),
    Record(
        "4", "8", "A*", "h_unmet_goal", 104, 34330, 34332, 328509, 14, 4.0136
    ),
    Record(
        "4",
        "10",
        "A*",
        "h_pg_maxlevel",
        104,
        62077,
        62079,
        599376,
        14,
        3268.4160,
    ),
]
df = pd.DataFrame(dataset)


# %%
df.head()


# %%

