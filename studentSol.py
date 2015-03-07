#!/usr/bin/env python3

import rpg

def get_clauses(merchant, level):
    clauses = []
    all_items = set()
    for abi in level.ability_names:
        this_abi = ()
        for equ in merchant.equipments:
            if abi in [x.name for x in equ.provides] :
                this_abi += (equ.index, )
                all_items.add(equ.index)
        clauses.append(this_abi)

    for e in merchant.equipments:
        clauses.append((-e.index, -e.conflicts.index))

    return clauses

def get_nb_vars(merchant, level):
    clauses = get_clauses(merchant, level)

    all_items = set()
    for elem in [elem for pair in clauses for elem in pair]:
        all_items.add(abs(elem))

    nb_vars = len(all_items)
    print(nb_vars)
    return nb_vars

