from djccx.inp.cards.SurfaceCard import SurfaceCard,SurfaceNodeCard
from djccx.inp.cards.NsetCard import NsetCard
from djccx.inp.cards.TieCard import TieCard
import re

# ===========================================
def remove_nset(self,name):
    def select(card):
        if isinstance(card,NsetCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
# ===========================================

def remove_surface(self,name):
    def select(card):
        if isinstance(card,SurfaceCard) or isinstance(card,SurfaceNodeCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
# ===========================================

def remove_surface_regex(self,regex):
    
    def select(card):
        if isinstance(card,SurfaceCard) or isinstance(card,SurfaceNodeCard):
            if re.fullmatch(regex,card.name):
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]
# ===========================================

def remove_nset_regex(self,regex):
    self.cards = [card for card in self.cards 
                    if not re.fullmatch(regex,card.name)]
# ==========================================

def remove_tie(self,name):
    
    def select(card):
        if isinstance(card,TieCard):
            if card.name == name:
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]

def remove_tie_regex(self,regex):
    def select(card):
        if isinstance(card,TieCard):
            if re.fullmatch(regex,card.name):
                return False
        return True
    self.cards = [card for card in self.cards 
                    if select(card)]