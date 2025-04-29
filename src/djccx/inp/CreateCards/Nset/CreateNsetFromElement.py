import numpy as np  # Import numpy for array operations
from djccx.inp.cards.NsetCard import NsetCard  # Import NsetCard to create node sets (nsets)

def CreateNsetFromElementIndex(self, index_el: list[int], name: str = None) -> NsetCard:
    """
    Creates a node set (nset) from the given element indices.

    Parameters:
    - self: The object containing the list of elements and nodes from the .inp file.
    - index_el (list[int]): A list of element indices from which the node set will be created.
    - name (str, optional): The name of the nset. If not provided, the name will default to the last element's ELSET.

    Returns:
    - NsetCard: The created nset (node set) containing unique nodes from the elements.
    """
    
    id_values_list = []  # Initialize an empty list to store node IDs

    # Iterate over the provided element indices
    for i in index_el:
        # Get unique nodes of the element at position 'i' and extract their IDs
        el = self.elements[i].GetUniqueNodes(self.nodes).index.values
        # Append node IDs to the list
        id_values_list.append(el)
    
    # Combine all the arrays of node IDs into a single array
    id_values_list = np.concatenate(id_values_list)

    # If no name is provided, use the ELSET option from the last processed element
    if name is None:
        name = self.elements[i].options["ELSET"]

    # Create a new NsetCard object using the name and the list of node IDs
    nset = NsetCard(name, id_values_list)

    # Append the created nset to the cards list (which holds all the components of the .inp file)
    self.cards = np.append(self.cards, nset)

    # Return the created node set (nset)
    return nset


def CreateNsetFromElement(self, elements: list, name: str) -> NsetCard:
    """
    Creates a node set (nset) from a list of elements.

    Parameters:
    - self: The object containing the list of elements and nodes from the .inp file.
    - elements (list): A list of element objects from which the node set will be created.
    - name (str): The name of the nset to be created.

    Returns:
    - NsetCard: The created nset (node set) containing unique nodes from the elements.
    """
    
    id_values_list = []  # Initialize an empty list to store node IDs

    # Iterate over each element in the provided list
    for element in elements:
        # Get unique nodes from the current element and extract their IDs
        id_values = element.GetUniqueNodes(self.nodes).index.values
        # Extend the list with the node IDs (add them all at once)
        id_values_list.extend(id_values)

    # Convert the list of node IDs into a numpy array for better handling
    id_values_list = np.array(id_values_list)

    # Create a new NsetCard object using the provided name and the node ID array
    nset = NsetCard(name, id_values_list)

    # Append the created nset to the cards list (which holds all the components of the .inp file)
    self.cards = np.append(self.cards, nset)

    # Return the created node set (nset)
    return nset
