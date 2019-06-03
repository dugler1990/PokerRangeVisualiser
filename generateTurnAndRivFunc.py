# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 22:23:47 2019

@author: dougl
"""
import itertools as it

toRemove =  [['Q','s'],['Q','d'],['K','s'],['T','s'],['9','s']]

Deck2 = treys.deck2.Deck2
Deck2._FULL_DECK = []
Deck2._FULL_DECK = Deck2.GetCustomDeck( *toRemove )



# Generate all turns and rivers

def GenerateTurnAndRiver(heroH,VilH,flop):

def GenerateTurnAndRivers(Deck, StringOutput = False):
    # Figure out how many combos:
    # = remaining cards Choose 2 without replace.
    CombosInt = list( itertools.combinations( Deck._FULL_DECK, 2  ) )
    CombosStr = []
    Combos = []
    if StringOutput == True:
        for i in range(CombosInt.__len__()):
            Card1 = Card.int_to_str(CombosInt[i][0])
            Card2 = Card.int_to_str(CombosInt[i][1])
            CombosStr.append([Card1,Card2])
            Combos = CombosStr
    else: Combos = CombosInt
    return Combos   