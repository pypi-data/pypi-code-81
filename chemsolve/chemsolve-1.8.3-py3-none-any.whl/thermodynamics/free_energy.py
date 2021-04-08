#!/usr/bin/env python3
# -*- coding = utf-8 -*-
import os

from chemsolve import Element, Compound
from chemsolve.reaction import Reaction
from chemsolve.utils.errors import InvalidReactionError

print(Reaction(reactants = (Element('H'), Compound('OH')), products = (Element('H2O'))))

