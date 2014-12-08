#!/usr/bin/env python3

import sys
import rpg
import minisat
import studentSol

def get_missing_abilities(solution_indexes):
  """
  Given the indexes of a solution, returns a list containing the names
  of the missing abilities
  """
  student_equipment = []
  for i in solution_indexes:
    if(i <= merchant.abi_base_index):
      student_equipment.append(merchant[i].name)
  #Checking the solution
  level_abilities = set(abi_name for abi_name in level.ability_names)
  for equ in equipment_sol:
    for abi in merchant[equ].provides:
      if abi.name in level_abilities:
        level_abilities.remove(abi.name)
  return list(level_abilities)

def get_violated_conflicts(solution_indexes):
  conflicts = []
  for equ in solution_indexes:
    if merchant[equ].conflicts.index in solution_indexes:
      conflicts.append((merchant[equ].name, merchant[equ].conflicts.name))
  return conflicts

def get_equipment_names(solution_indexes):
  equ_names = []
  for i in solution_indexes:
    if(i <= merchant.abi_base_index):
      print(merchant[i].name)
  return equ_names

def default_usage():
  # The first argument must reference a merchant file and the second argument must represent a level file
  print("Usage:", sys.argv[0], "MERCHANT_FILE LEVEL_FILE", file=sys.stderr)
  exit(1)


if __name__ == "__main__":
  if len(sys.argv) != 3:
    default_usage()

  merchant = rpg.Merchant(sys.argv[1])
  level = rpg.Level(sys.argv[2])
  level_num_str = sys.argv[2].split("_")[1].split(".")[0]

  clauses = studentSol.get_clauses(merchant, level)
  nb_vars = studentSol.get_nb_vars(merchant, level)

  sol = minisat.minisat(nb_vars, clauses)

  equipment_sol = []
  if sol:
    equipment_sol = [eq for eq in sol if eq <= merchant.abi_base_index]

  missing_abilities = get_missing_abilities(equipment_sol)
  violated_conflicts = get_violated_conflicts(equipment_sol)

  if missing_abilities:
    print("MISSING ABILITIES: " + str(len(missing_abilities)))
    for abi in missing_abilities:
      print(abi)

  if violated_conflicts:
    print("VIOLATED CONFLICTS: " + str(len(conflicts)))
    for conf in conflicts:
      print(str(conf))

  if not (missing_abilities or violated_conflicts):
    print("INSTANCE SOLVED")
    print("You defeated level " + level_num_str + " with " + str(len(equipment_sol)) + " equipment pieces.")
