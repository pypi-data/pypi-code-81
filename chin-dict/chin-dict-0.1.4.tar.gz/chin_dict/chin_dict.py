# TODO can see traditional/simplified form

from .chindict import ChinDict 
import argparse

__version__ = "0.1.4"

parser = argparse.ArgumentParser(description='Lookup character or word')

parser.add_argument('character', type=str, help='Character to search')
group = parser.add_mutually_exclusive_group()
group.add_argument('-w', '--word', action='store_true', help='lookup word')
group.add_argument('-t', '--tree', action='store_true', help='show tree')
group.add_argument('-tm', '--treemean', nargs=1, type=int, help='show tree')
group.add_argument('-c', '--comp', action='store_true', help='show components')
group.add_argument('-cm', '--compmean', action='store_true', help='show component meanings')
group.add_argument('-r', '--rad', action='store_true', help='show radical')
group.add_argument('-rm', '--radmean', action='store_true', help='show radical meaning')

#parser.add_argument('component_index', nargs="?", type=int, help='Index of component')

args = parser.parse_args()


def main():
        
    hd = ChinDict(charset='simplified')

    if args.word:
        res = hd.lookup_word(args.character)
        print("-----------------------------")
        for word in res:
            print(word)
    else:
        
        res = hd.lookup_char(args.character)
        print("-----------------------------")

        if args.tree:
            res.tree()
        elif args.comp:
            try:
                print(res.components)
            except AttributeError:
                print(res.character + " has no components.")
        elif args.rad:
            try: 
                print(res.radical)
            except AttributeError:
                print(res.character + " has no radical.")
        elif args.radmean:
            try: 
                print(res.radical.meaning)
            except AttributeError:
                print(res.character + " has no radical.")
        elif args.compmean:
            try:
                for comp in res.components:
                    print(comp.character + " meaning(s):")
                    print(comp.meaning)
                    print()
            except AttributeError:
                print(res.character + " has no components.")
        elif args.treemean:
            try:
                res.tree(False)
                try:
                    comp = res._component_list[args.treemean[0] - 1]
                    print(comp.character + " meaning(s):")
                    print(comp.meaning)
                    print()
                except IndexError:
                    print("Component index out of range.")
                    
            except AttributeError:
                print(res.character + " has no components.")

        else:
            print("Character:", res.character)
            print("Pinyin:", res.pinyin)
            print("Meaning:", res.meaning)
