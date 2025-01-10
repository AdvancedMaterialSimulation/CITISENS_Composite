import pandas as pd
import numpy as np
def CreateNsetFromElset(inp_f,elset,name=None):

    elements = inp_f.elements
    # only 2d 
    elements = [ iel for iel in elements if iel.elements.shape[1] == 6]

    all_id_elements = np.concatenate([ iel.eid for iel in elements ])
    all_elements    = [ iel.elements for iel in elements ]
    all_elements = np.concatenate(all_elements)


    # index all_id_elements is a unique identifier and all_elements is the column 
    df_elements = pd.DataFrame(all_elements, index=all_id_elements)

    points_fcn = lambda elset: np.unique(np.concatenate(df_elements.loc[elset.id_elements].values))

    points_x0 = points_fcn(elset)

    return inp_f.CreateNsetFromIds(points_x0,name=name)