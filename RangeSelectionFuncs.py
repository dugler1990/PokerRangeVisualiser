# Equity vs Range: vilRange, HeroHand,

# Generate Example VilRange, [[],[]]
#vilRange = ['Q,8s', 'Q,7s', 'Q,6s', 'J,8s', 'J,7s', 'j,6s', '10,8s', '10,7s', '10,6s', '9,8s', '9,7s', '9,6s', '8,8', '8,7s', '8,6s', '7,8', '7,7', '7,6s', '8,6', '7,6', '6,6', '8,5', '7,5', '6,5', '8,4', '7,4', '6,4']

# --> see what the Output of the range selector looks like to use something like that. 
import itertools
import datetime as DT
import sys
import treys
from treys import Evaluator
from treys import Card
from treys import Deck2   # If this were to be used as jjust Deck, i may have a problem defining a variable as 'Deck' maybe use myDeck as var

def GenerateTurnAndRivers( myDeck, StringOutput = False):
    # Figure out how many combos:
    # = remaining cards Choose 2 without replace.
    CombosInt = list( itertools.combinations( myDeck._FULL_DECK, 2  ) )    # not sure if it should be .cards i think it should be ! i hope no error...
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



def EquityVsRange(vilRange, heroHand, flop):
    handEval = Evaluator()
    WIN = 0
    LOOSE = 0

    # vilRange will come as defined above, heroHand as writen in input for now, flop same.
    
    ############## Factorize func
    toRemove = [] 
    #toRemoveString = [] ### its already in some kind of string format....Pass toRemove, Create 'Qs' type string, before creating hand, check its plausible.
    for i in range(flop.__len__()):
        cardTempstr = Card.int_to_str(flop[i])
        cardRankTemp = cardTempstr[0]
        cardSuitTemp = cardTempstr[1]
        
        toRemove.append([cardRankTemp, cardSuitTemp])
    for i in range(heroHand.__len__()):
        cardTempstr = Card.int_to_str(heroHand[i])
        cardRankTemp = cardTempstr[0]
        cardSuitTemp = cardTempstr[1]
        
        toRemove.append([cardRankTemp, cardSuitTemp])   # we need to remove the vilains cards from the deck each time.....in fact this is a frikin issue.
     ############# Factorize func above 

    myDeck = treys.deck2.Deck2()

    for HAND in range(vilRange.__len__()):     # could probably more efficient without range and HAND = numeric hand val. (efficiency)(e1)
        vilHandTemp = vilRange[HAND] # I need to convert suited and non-suited hands into actual sets of cards.... ooor. loop around all possibilities.
        vilHandCombos = rangeSelectorValueToHandList( vilHandTemp, toRemove)#(e1)
        #print(vilHandCombos[0][0])
        for COMBO in range(vilHandCombos.__len__()):            
            # Villain Hand for now Default AcAs
            vilHand = [
                    Card.new( Card.int_to_str( vilHandCombos[COMBO][0] )  ),
                    Card.new( Card.int_to_str( vilHandCombos[COMBO][1] )  )
                    ]
#            print('vilHand:')
#            print(vilHand)
            for V in range(vilHand.__len__()):
                cardTempstr = Card.int_to_str(vilHand[V])
                cardRankTemp = cardTempstr[0]
                cardSuitTemp = cardTempstr[1]
                if V == 0: 
                    toRemoveTemp = toRemove.copy()
#                    print('redefined toRemoveTemp :')
#                    print('toRemove V=0')
#                    print(toRemove)
#                    print('toRemoveTemp V=0')
#                    print(toRemoveTemp)
#                print('toRemoveTemp prior to append'+str(V) )
#                print(toRemoveTemp)
#                print('Card to append')
#                print([cardRankTemp, cardSuitTemp])
                toRemoveTemp.append([cardRankTemp, cardSuitTemp])
           #print('toRemove after adding hands')
           #print(toRemoveTemp)
            myDeck.GetCustomDeck( *toRemoveTemp )  
            possibleTurnAndRiver = GenerateTurnAndRivers(myDeck, StringOutput = False)        
        
            for TnR in range(possibleTurnAndRiver.__len__()):
                #print(TnR)
                #print(tuple(flop)  )
                #print( possibleTurnAndRiver[TnR] )
                flopTemp = tuple(flop) + possibleTurnAndRiver[TnR]
#                print(type(vilHand))
#                print(type(flopTemp))
#                print('Inputs to handEval that is failing:')
#                print(vilHand)
#                print(heroHand)
#                print(list(flopTemp))
                ResultsVil = handEval.evaluate( vilHand, list(flopTemp) )
                ResultsHero =  handEval.evaluate( heroHand, list(flopTemp) )
#                print(ResultsVil)
#                print(ResultsHero)
            
                if ResultsHero < ResultsVil:
                    WIN = WIN + 1
                if ResultsHero > ResultsVil:
                    LOOSE = LOOSE + 1
                if ResultsHero == ResultsVil:
                    LOOSE = LOOSE + 0.5
                    WIN = WIN + 0.5
                    
                    
    # Calc Equity:

    # No tie Equity = win/win+loose
    # When people talk about the equity in their hand, they win they %win...
    #->  BOARD = A A A A K , both have 0 % to win

    # Upon tying, i could add 0.5 to each counter. This makes good sense. in the above example equity = 50% correct

    # intuitivly this seems correct to me, we could confirm this results vs something else.    
                    
    Equity = WIN / (WIN + LOOSE)
    Equity = round(Equity,3)
    return(Equity)             

def rangeSelectorValueToHandList(HandStr, toRemove): # I think Ideally it should use Deck where Deck has as new method to check what missing suits a rank has, to create the suit list used previously....im sure i could be even smarter.
    
    # Passing 'toRemove' is easy...
    
    #print(HandStr)
    
    # if 's' its all the same suit combos, else all the non-suited combos.
    
    # (i) !! The suit definitions could be taken from the Deck class. 1. Not very important, 2. this is not a class method....although it could be.
    SUITS = ['s','h','d','c']   #### The deck does not contain these suits for that card currently , we should generate this value inteligently
    
    ##### Using Deck this can clearly be optimized, but for now : SUITS = Deck.
    
    
    SUITED = HandStr.find('s')
    Pair = False
    if HandStr[0] == HandStr[2]: 
        Pair = True
    Combos = []
    CombosStr = []
    if SUITED == -1 and Pair == False:
        # non-suited combos
        #print(HandStr)
        Card1Str = HandStr[0]
        Card2Str = HandStr[2]
        
        suitCombos = list( itertools.permutations(SUITS,2 ) )
        for i in range(suitCombos.__len__()):
            if ([Card1Str ,  suitCombos[i][0]] in toRemove or [Card2Str ,  suitCombos[i][0]] in toRemove ):
                pass
            else:
                try:
                    Combos.append( [ Card.new( str( Card1Str +  suitCombos[i][0] ) ),Card.new( str( Card2Str +  suitCombos[i][1] ) ) ] )
                    CombosStr.append( [str( Card1Str +  suitCombos[i][0] ) , str( Card2Str +  suitCombos[i][1] )  ] )
                except:
                    print(str( Card2Str +  suitCombos[i][1] ) + Card1Str +  suitCombos[i][0] + ' not in deck slowin us downnn')
    
    elif Pair == True:
        # pair combos
        #print(HandStr)
        Card1Str = HandStr[0]
        Card2Str = HandStr[2]
        
        suitCombos = list( itertools.combinations(SUITS,2 ) )

        for i in range(suitCombos.__len__()):
            if ([Card1Str ,  suitCombos[i][0]] in toRemove or [Card2Str ,  suitCombos[i][1]] in toRemove ):
                pass
            else:
                try:
                    Combos.append( [ Card.new( str( Card1Str +  suitCombos[i][0] ) ),Card.new( str( Card2Str +  suitCombos[i][1] ) ) ] )
                    CombosStr.append( [str( Card1Str +  suitCombos[i][0] ), str( Card2Str +  suitCombos[i][1] )  ] )

                except:
                    print(str( Card2Str +  suitCombos[i][1] ) + Card1Str +  suitCombos[i][0] + ' not in deck slowin us downnn')
        
    else:
        # suited combos.
#        print(HandStr)
        HandStr = HandStr.replace('s','')
        Card1Str = HandStr[0]
        Card2Str = HandStr[2]
        for i in range(SUITS.__len__()):
#            print(str([Card1Str ,  SUITS[i] ]))
#            print(str([Card2Str ,  SUITS[i] ]))
#
#            print( toRemove)
            if ([Card1Str ,  SUITS[i]] in toRemove or [Card2Str ,  SUITS[i]] in toRemove ):
                pass
            else:
                try:
                    Combos.append( [ Card.new( str( Card1Str + SUITS[i] ) ),Card.new( str( Card2Str + SUITS[i] ) ) ] )
                except:
                    print(str( Card2Str +  SUITS[i] ) +Card1Str +  SUITS[i] + ' not in deck slowin us downnn')
    return(Combos) 


def separateCardsByComma(Boardstr):
        commaCount = Boardstr.count(',')
        Board = []
        prevComma = 0
        for i in range( 0,commaCount+1 ):
            if i != 0:
                prevComma = BoardstrTemp.index(',')
                BoardstrTemp = BoardstrTemp[ BoardstrTemp.index(',') + 1: BoardstrTemp.__len__() ]
            else:
                BoardstrTemp = Boardstr
            if i != commaCount:
                commaIndexTemp = BoardstrTemp.index(',')
            else:
                commaIndexTemp = BoardstrTemp.__len__()
            print(BoardstrTemp[ 0 : commaIndexTemp] )
            Board.append(Card.new( BoardstrTemp[ 0 : commaIndexTemp] ) )
        return(Board)