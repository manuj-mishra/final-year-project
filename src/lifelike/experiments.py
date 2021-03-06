import csv
from random import random

import numpy as np
import pandas as pd

from lifelike.CAs import GRID_SIZE
from lifelike.Population import Population
from lifelike.constants import CHROMOSOME_LEN
from util import binary
#HYPERPARAMETER TUNING
if __name__ == "__main__":
  with open('goals.npy', 'rb') as goalfile:
    goals = np.load(goalfile)

  with open('ics.npy', 'rb') as icfile:
    ics = np.load(icfile)

  for max_step in (1, 5, 10):
    for eval_step in (1, 5, 10):
      pop_size = 20
      elitism = 0.2
      mutation = 1 / CHROMOSOME_LEN
      epoch_n = 30
      hyperparams = {
        "max_step": max_step,
        "eval_step": eval_step,
      }
      exp_name = f"single_max{max_step}_eval{eval_step}"
      print(f"Running {exp_name}")
      rules = []
      conv_epochs = []
      num_visited = []
      best_rules = []
      pcount = 0
      for goalarr in goals:
        print(pcount)
        rules.append(goalarr)
        trueB = binary.ones(goalarr >> (CHROMOSOME_LEN // 2))
        trueS = binary.ones(goalarr)
        pop = Population(pop_size, elitism, mutation, trueB, trueS, ics, 'binary', hyperparams)
        counter = 0
        for _ in range(epoch_n):
          if pop.goal_found():
            break
          pop.iterate()
          counter += 1
        conv_epochs.append(counter)
        num_visited.append(len(pop.visited))
        best_rules.append(pop.inds[0].rstring)
        pcount += 1

      df = pd.DataFrame({"rstring": rules,
                         "convtime": conv_epochs,
                         "visited": num_visited,
                         "bestrule": best_rules})
      df.to_csv(f"./{exp_name}.csv")
