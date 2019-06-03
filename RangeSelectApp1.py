# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 16:49:23 2019

@author: dougl
"""





import itertools
import datetime as DT
import sys
import treys
from treys import Evaluator
from treys import Card
from treys import Deck
from treys import Deck2
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

# source functions
from RangeSelectionFuncs import rangeSelectorValueToHandList
from RangeSelectionFuncs import separateCardsByComma
from RangeSelectionFuncs import GenerateTurnAndRivers
from RangeSelectionFuncs import EquityVsRange

Ui_MainWindow, QtBaseClass = uic.loadUiType("C:\\Users\\dougl\\Desktop\\Data Blog\\PythonPoker\\qtRangeSelectorAttempt1.ui")

# Declare global variables:
vilRange = []


class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.get_Range_Button.clicked.connect(self.selectRange)
        self.ui.listUpdate_Button.clicked.connect(self.listUpdate)
        self.ui.EvalHand_Button.clicked.connect(self.HeroVsRangeEquityCalc)
    def selectRange(self):
        RANGE = self.ui.rangeWidget.selectedItems()
        self.ui.textEdit_2.setPlainText(RANGE.__str__())
        self.ui.textEdit.setText(str(RANGE[0]))
    def listUpdate(self):
        global vilRange
        vilRange = []
        RANGE = self.ui.rangeWidget.selectedItems()
        self.ui.listWidget.clear()
        for i in range(0,RANGE.__len__()):
            vilRange.append( RANGE[i].text() )
            textTemp = RANGE[i].text()
            self.ui.listWidget.addItem(textTemp )
        #print(vilRange)
   
    def HeroVsRangeEquityCalc(self):
        global vilRange
        START = DT.datetime.now()
        # Hero Hand
        heroHandstr = self.ui.heroHand.toPlainText()
        
        heroCard1 = Card.new(heroHandstr[0:2])
        heroCard2 = Card.new(heroHandstr[3:5])
        
        heroHand = [
            heroCard1,
            heroCard2
        ] # This is not going to work on 10 ---- need to search for commas or sumn like below. 10 = T
       
        # Board
        Boardstr = self.ui.board.toPlainText()
        
        ### Func to be extracted to Loose file func(str,',') -> nCardList
        # Break up text by comma
        Board = separateCardsByComma( Boardstr ) ## Functio nname should be better
        
        ### END FUN TO BE EXTRACTED 
        

        # Evaluate Equity
        
        Equity = EquityVsRange( vilRange, heroHand, flop = Board)
       
            
        self.ui.EvalTextDisplay.setPlainText(str(Equity) )
        END = DT.datetime.now()
        TIME = END - START
        print(TIME.seconds)
        
       

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())