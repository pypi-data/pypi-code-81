# -*- coding: utf-8 -*-
"""
@author: T. Malfatti <malfatti@disroot.org>
@date: 20170704
@license: GNU GPLv3 <https://gitlab.com/malfatti/SciScripts/raw/master/LICENSE>
@homepage: https://gitlab.com/Malfatti/SciScripts
"""

from xml.etree import ElementTree


def Root2Dict(El):
    Dict = {}
    if El.getchildren():
        for SubEl in El:
            if SubEl.keys():
                if SubEl.get('name'):
                    if SubEl.tag not in Dict: Dict[SubEl.tag] = {}
                    Dict[SubEl.tag][SubEl.get('name')] = Root2Dict(SubEl)

                    Dict[SubEl.tag][SubEl.get('name')].update(
                        {K: SubEl.get(K) for K in SubEl.keys() if K is not 'name'}
                    )

                else:
                    Dict[SubEl.tag] = Root2Dict(SubEl)
                    Dict[SubEl.tag].update(
                        {K: SubEl.get(K) for K in SubEl.keys() if K is not 'name'}
                    )

            else:
                if SubEl.tag not in Dict: Dict[SubEl.tag] = Root2Dict(SubEl)
                else:
                    No = len([k for k in Dict if SubEl.tag in k])
                    Dict[SubEl.tag+'_'+str(No+1)] = Root2Dict(SubEl)

        return(Dict)
    else:
        if El.items(): return(dict(El.items()))
        else: return(El.text)

def ReadTree(File):
    Tree = ElementTree.parse(File)
    Root = Tree.getroot()
    return(Tree, Root)

## Level 1
def Read(File):
    Root = ReadTree(File)[1]
    Info = Root2Dict(Root)
    return(Info)

