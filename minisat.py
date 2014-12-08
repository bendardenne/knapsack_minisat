"""Helper module to call minisat."""

import os
import tempfile


def minisat(n, clauses, executable="./minisat"):
  """Run Minisat on the given set of clauses. Return None if the clauses are
  unsatisfiable, or a solution that satisfies all the clauses (a sequence of
  integers representing the variables that are true).

  Arguments:
  n -- number of variables (each variable is denoted by an integer within the
    range 1..n)
  clauses -- sequence of clauses. Each clause is a tuple of integers
    representing the literals: a positive integer for a variable, a
    negative integer for the negated variable.
  executable -- name of the MiniSat executable to run

  Example:
  Consider a vocabulary with 3 variables A, B, C and the clauses !A || B,
  !B || !C and A.

  >>> minisat(3, [(-1, 2), (-2, -3), (1,)])
  [1, 2]

  meaning the clauses are satisfiable and {A=True, B=True, C=False} is a
  model."""
  clause_path = "clauses.tmp"
  sol_path = "sol.tmp"
  out_path = "minisat.out"
  try:
    # Creating and writing the clause file
    clause_file = open(clause_path, "wt")
    print("p cnf", n, len(clauses), file=clause_file)
    for c in clauses:
      print(" ".join(str(l) for l in c), "0", file=clause_file)
    clause_file.close()
    # Reading the sol file
    os.system("%s %s %s > %s" % (executable, clause_path, sol_path, out_path))
    out_file = open(sol_path)
    if out_file.readline().strip() == "UNSAT":
      return None
    else:
      return [int(x) for x in out_file.readline().strip().split(" ")
              if int(x) > 0]
  finally:
    try:
      out_file.close()
      os.remove(clause_path)
      os.remove(sol_path)
    except:
      pass

