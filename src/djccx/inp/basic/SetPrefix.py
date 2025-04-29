
def SetPrefix(inp2,prefix):
    for element in inp2.elements:
        element.name = element.name.replace("ELSET=", "ELSET="+prefix)
        element.options["ELSET"] = prefix+element.options["ELSET"]
        # nset

    for elsetofelset in inp2.elsetsofelsets:
        elsetofelset.name = prefix + elsetofelset.name 
        elsetofelset.name_up = prefix.upper() + elsetofelset.name_up
        for ide in range(len(elsetofelset.id_elements)):
            elsetofelset.id_elements[ide] = prefix + elsetofelset.id_elements[ide]

    cards_sets = [ inp2.elsets, 
                    inp2.nsets, 
                    inp2.surfaces, 
                    inp2.surface_interactions, 
                    inp2.ties, 
                    inp2.materials]
    
    for cards in cards_sets:
        for card in cards:
            card.name = prefix + card.name 
            card.name_up = prefix.upper() + card.name_up

