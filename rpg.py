""" Helper module for the equipment problem"""

import gzip


class Equipment:
  """A wearable equipment.

  Members:
  index -- index in the merchant inventory
  name -- the name of the equipment
  conflicts -- equipment that conflicts with this equipment
  provides -- set of ability names this equipment provides
  
  """

  def __init__(self, index, name):
    self.index = index
    self.name = name
    self.conflicts = self
    self.provides = set()

  def __repr__(self):
    return "<Equipment {}>".format(self.name)

  def __str__(self):
    return self.name

class Ability:
  """An ability for the player.

  Members:
  index -- index in the merchant inventory
  name -- the name of the ability
  provided_by -- set of equipment names providing this ability
  
  """

  def __init__(self, index, name):
    self.index = index
    self.name = name
    self.provided_by = set()

  def __repr__(self):
    return "<Ability {}>".format(self.name)

  def __str__(self):
    return self.name

class Merchant:
  """A merchant inventory is a collection of equipments. Equipments are indexed starting
  from 1, Abilities are indexed starting from nbEquipments + 1"""
  
  def __init__(self, filename):
    """Load a gzipped equipment list."""
    self.equipments = []
    self.abilities = []
    self.abi_base_index = 0
    self.equ_map = {}
    self.abi_map = {}

    def get_equ(name):
      if name not in self.equ_map:
        equ = Equipment(len(self.equipments) + 1, name)
        self.equipments.append(equ)
        self.equ_map[name] = equ
      return self.equ_map[name]

    def get_abi(name):
      if name not in self.abi_map:
        abi = Ability(len(self.abilities) + 1 + self.abi_base_index, name)
        self.abilities.append(abi)
        self.abi_map[name] = abi
      return self.abi_map[name]

    with gzip.open(filename) as f:
      current = None
      for line in f:
        line = line.decode().strip()
        if not line:
          continue
        cmd = line[:line.index(":")]
        args = line[line.index(":") + 1:]
        if cmd == "Size":
          self.abi_base_index = int(args.strip())
        elif cmd == "Equipment":
          current_equ = get_equ(args.strip())
        elif cmd == "Abilities":
          current_equ.provides = set(get_abi(a.strip())
                        for a in args.split(", "))
          for a in args.split(", "):
            current_abi = get_abi(a.strip())
            current_abi.provided_by.update([current_equ])
        elif cmd == "Conflicts":
          current_equ.conflicts = get_equ(args.strip())

  def __len__(self):
    return len(self.equipments)

  def __contains__(self, x):
    if isinstance(x, Equipment):
      x = x.name
    return x in self.map

  def __getitem__(self, x):
    if isinstance(x, int):
      return self.equipments[x - 1]
    else:
      return self.map[x]

  def __iter__(self):
    return iter(self.equipments)

class Level:
  """A level is a collection of enemies. To each enemy corresponds
  a set of abilities needed in order to defeat it."""
  
  def __init__(self, filename):
    """Load a gzipped enemy list."""
    self.enemy_names = []
    self.ability_names = []

    def get_abi(name):
      if name not in self.ability_names:
        self.ability_names.append(name)
      return name

    def get_ene(name):
      if name not in self.enemy_names:
        self.enemy_names.append(name)
      return name

    with gzip.open(filename) as f:
      current = None
      for line in f:
        line = line.decode().strip()
        if not line:
          continue
        cmd = line[:line.index(":")]
        args = line[line.index(":") + 1:]
        if cmd == "Enemy":
          current_ene = args.strip()
          get_ene(current_ene)
        elif cmd == "Requirements":
          for a in args.split(", "):
            get_abi(a.strip())

  def __len__(self):
    return len(self.ability_names)

  def __contains__(self, x):
    return x in self.ability_names

  def __getitem__(self, x):
    return self.ability_names[x]

  def __iter__(self):
    return iter(self.ability_names)