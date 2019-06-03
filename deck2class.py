from random import shuffle
from .card import Card

class Deck2:
    """
    Class representing a deck. The first time we create, we seed the static 
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it. 
    """
    _FULL_DECK = []

    def __init__(self):
        self.shuffle()

    def shuffle(self):
        # and then shuffle
        self.cards = Deck2.GetFullDeck()
        shuffle(self.cards)

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)

        cards = []
        for i in range(n):
            cards.append(self.draw())
        return cards

    def __str__(self):
        return Card.print_pretty_cards(self.cards)

    @staticmethod
    def GetFullDeck():
        if Deck2._FULL_DECK:
            return list(Deck2._FULL_DECK)

        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit,val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                Deck2._FULL_DECK.append(Card.new(rank + suit))
        return list(Deck2._FULL_DECK)       
   # @staticmethod i believe static methods should not take parametres.
    def GetCustomDeck( *toRemove ):
        #if Deck2._FULL_DECK:
         #   return list(Deck2._FULL_DECK)
        Deck2._FULL_DECK = []
        # create the standard 52 card deck
        for rank in Card.STR_RANKS:
            for suit,val in Card.CHAR_SUIT_TO_INT_SUIT.items():
                if [rank,suit] in toRemove:
                    pass
                    #print([rank,suit])
                else:Deck2._FULL_DECK.append(Card.new(rank + suit))
        return list(Deck2._FULL_DECK)
                
    def removeCardByInt( self, cardInt ):
        if cardInt in self.cards:
            self.cards.remove(cardInt)
        else: print('The Card did not exist in the deck')


        