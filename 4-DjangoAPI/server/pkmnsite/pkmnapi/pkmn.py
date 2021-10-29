# -*- coding: utf-8 -*-
import json
import re

from .models import *


class PkmnDict(dict):
    def __init__(self, pkmn_as_dict):
        dict.__init__(self)
        self.update(pkmn_as_dict)

    @staticmethod
    def read_data(json_binary):
        # type: (bytes) -> [PkmnDict]
        json_unicode = json_binary.decode("utf-8")
        return PkmnDict.parse(json_unicode)

    @staticmethod
    def parse(json_unicode):
        # type: (str) -> [PkmnDict]
        as_list_of_dicts = json.loads(json_unicode)

        pkmn_dicts_list = []
        for _pkmn in as_list_of_dicts:
            new_obj = PkmnDict(_pkmn)
            pkmn_dicts_list.append(new_obj)
        return pkmn_dicts_list

    def is_legendary(self):
        # type: (PkmnDict) -> bool
        return self.get("Legendary", False)

    def is_type(self, pkmn_type):
        # type: (PkmnDict,str) -> bool
        pkmn_types = []
        keys = self.keys()
        keys_sorted = sorted(keys)
        for k in keys_sorted:
            m = re.match(r"^Type \d+$", k)
            if m != None:
                pkmn_types.append(self[k])
        return pkmn_type in pkmn_types

    def add_to_db(self):
        # type: (PkmnDict) -> None

        #################################
        # Apply filter and other requests

        # Exclude Legendary Pokémon
        if self.is_legendary():
            return

        # Exclude Pokémon of Type: Ghost
        if self.is_type("Ghost"):
            return

        # For Pokémon of Type: Steel, double their HP
        if self.is_type("Steel"):
            hp = self["HP"]
            self["HP"] = hp * 2

        # For Pokémon of Type: Fire, lower their Attack by 10%
        if self.is_type("Fire"):
            attack = self["Attack"]
            self["Attack"] = int(attack - (attack * 0.1))

        # For Pokémon of Type: Bug & Flying, increase their Attack Speed by 10%
        if self.is_type("Bug") and self.is_type("Flying"):
            attack = self["Attack"]
            self["Attack"] = int(attack + (attack * 0.1))
            speed = self["Speed"]
            self["Speed"] = int(speed + (speed * 0.1))

        # For Pokémon that start with the letter G, add +5 Defense for every letter in their name (excluding G)
        if self["Name"].startswith("G"):
            name = self["Name"]
            letter_only_name = re.sub(r'[^a-zA-Z]', '', name)
            letter_only_name_no_G = re.sub(r'G', '', letter_only_name)

            count = len(letter_only_name_no_G)
            defence = self["Defense"]
            self["Defense"] = defence + count * 5

        ###########################################
        # Add each dict to db
        pkmn_inst = PkmnModel(id=self.get("#", None),
                              name=self.get("Name", None),
                              type1=self.get("Type 1", None),
                              type2=self.get("Type 2", None),
                              hp=self.get("HP", None),
                              attack=self.get("Attack", None),
                              defense=self.get("Defense", None),
                              sp_atk=self.get("Sp. Atk", None),
                              sp_def=self.get("Sp. Def", None),
                              speed=self.get("Speed", None),
                              generation=self.get("Generation", None),
                              legendary=self.get("Legendary", None))

        pkmn_inst.save()
