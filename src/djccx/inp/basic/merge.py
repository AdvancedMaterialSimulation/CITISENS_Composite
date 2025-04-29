import numpy as np
import pandas as pd

def merge(inp1,inp2,prefix=""):
    # merge two inps
    # get the last node id of inp1
    last_node_id = inp1.last_node_id()
    # add the last node id to inp2
    last_ele_id = inp1.last_element_id()
    inp2.nodes.df.index += last_node_id

    # reset elements id
    inp2 = inp2.reset_index(last_node_id,last_ele_id)
    # all name of elements  in inp2 must be changed to prefix

    card_2 = inp2.cards
    for cards in card_2:
        cards.name = prefix + cards.name
        cards.name_up = prefix.upper() + cards.name_up

    inp1.nodes.df = pd.concat([inp1.nodes.df,inp2.nodes.df])

    # add the elements of inp2 to inp1
    #inp1.elements = np.append(inp1.elements,inp2.elements)
    # add the cards of inp2 to inp1
    # remove nodeCard of inp2
    inp2.cards = [card for card in inp2.cards 
                    if card.type != '*NODE']
    inp2.cards = [card for card in inp2.cards 
                    if card.type != 'None']

    inp1.cards = np.append(inp1.cards,inp2.cards)
    return inp1