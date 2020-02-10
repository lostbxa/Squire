import json
import os

STATS = ['NAME', 'STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
ITM = ['NAME', 'WEIGHT', 'QTY', 'COST', 'DESCRIPTION']


def load_character(name):
    cf = open(name + "/" + name + ".cf")
    c = Character()
    c.stats= json.load(cf)
    inf = open(name + "/" + name + ".inf")
    c.Inventory = json.load(inf)
    print("Character loaded. Name: " + c.stats["NAME"])
    return c


class Character:
    def __init__(self, name=None, str=None, dex=None, con=None, int=None, wis=None, cha=None, gold=None, color=None, items=None):
        self.stats = {
            'NAME': name,
            'STR': str,
            'DEX': dex,
            'CON': con,
            'INT': int,
            'WIS': wis,
            'CHA': cha
        }
        self.Inventory = {}

    def save_character(self):
        try:
            cf = open(self.stats['NAME']+"/"+self.stats['NAME']+".cf", "w")
        except FileNotFoundError:
            try:
                os.mkdir((self.stats['NAME']))
            except OSError:
                print("Could not create directory")
                raise CharacterError("Holup, I fucked up")
        else:
            ch = json.dumps(self.stats)
            cf.write(ch)
            inf = open(self.stats['NAME']+"/"+self.stats['NAME']+".inf", "w")
            inv = json.dumps(self.Inventory)
            inf.write(inv)



    def set_val(self, name, value):
        if name in STATS:
            self.stats[name] = value
        elif name == 'color':
            self.Inventory["Button"] = {'NAME': 'Button',
                                        'WEIGHT': 0.01,
                                        'QTY': 1,
                                        'COST (GP)': 0.0001,
                                        'DESCRIPTION': 'A {} colored button given to you by Xephyr'.format(value.lower())
                                        }

    def add_item(self, name, desc):
        self.Inventory[name] = desc

class CharacterError(RuntimeError):
    def __init__(self, arg):
        self.args = arg