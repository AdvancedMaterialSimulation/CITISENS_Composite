from AnalyticalLayers.models_tl_free import Tau_model,E_flexion,E_Tensile,Fraction_Carbon
import numpy as np
import pandas as pd
nu = 0.4

theta = lambda x: 0.5 + 0.5*np.tanh(100*x)
relu  = lambda x: x*theta(x)

def objetive(radius,tn,tl,En,El,df,give_pred=False):

    t_p = [ Tau_model(ilayer, tn, tl) for ilayer in df["layers"]]
    t_p = np.array(t_p)


    Et_p =  [E_Tensile(En, El, tn, tl, ilayer ) for ilayer in df["layers"]]
    Et_p = np.array(Et_p)


    #El_f = 2*El/(1-nu**2)

    # El_f = 2*El
    El_f = El
    Eb_p =  [E_flexion(En, El_f, tn, tl, ilayer ) for ilayer in df["layers"]]
    #Eb_p = np.array(Eb_p)*(1-nu**2)

    Vc = [ Fraction_Carbon(radius,tn,tl,ilayer) for ilayer in df["layers"]]


    error_t   = 100*abs(df["t [mm]"]   - t_p )/df["t [mm]"]
    error_Et  = 100*abs(df["Et [GPa]"] - Et_p)/df["Et [GPa]"]
    error_Eb  = 100*abs(df["Eb [GPa]"] - Eb_p)/df["Eb [GPa]"]
    error_Vc  = 100*abs(df["Vc"]      - Vc )/df["Vc"]

    if give_pred:
        pred_df = pd.DataFrame({
            "t [mm]"  : t_p,
            "Et [GPa]": Et_p,
            "Eb [GPa]": Eb_p,
            "Vc"      : Vc   
        })

        error_df = pd.DataFrame({
            "t [%]"  : error_t,
            "Et [%]": error_Et,
            "Eb [%]": error_Eb,
            "Vc [%]": error_Vc
        })
        return pred_df, error_df
    else:

        L_t  = (error_t**2).mean()
        L_Et = (error_Et**2).mean()
        L_Eb = (error_Eb**2).mean()
        L_Vc = (error_Vc**2).mean()

        # En < all(El)
        L_mul = 0*1e3*relu( En - np.max(El) )

        return  L_t + L_Eb + L_Et + L_mul + L_Vc