from AnalyticalLayers.models import Fraction_Carbon_2
import numpy as np
import pandas as pd
nu = 0.4

theta = lambda x: 0.5 + 0.5*np.tanh(100*x)
relu  = lambda x: x*theta(x)

def objetive(radius,tn,tl,df,give_pred=False):


    Vc = [ Fraction_Carbon_2(radius,tn,tl,ilayer) 
            for ilayer in df["layers"]]

    error_Vc  = 100*abs(df["Vc"]      - Vc )/df["Vc"]
    if give_pred:
        pred_df = pd.DataFrame({
            "Vc"      : Vc   
        })

        error_df = pd.DataFrame({
            "Vc [%]": error_Vc,
        })
        return pred_df, error_df
    else:

        L_Vc = (error_Vc**2).mean()
    
        return L_Vc 
