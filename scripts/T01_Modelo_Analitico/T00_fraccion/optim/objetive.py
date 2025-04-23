from AnalyticalLayers.models import Tau_model       ,\
                                    E_flexion       ,\
                                    E_Tensile       ,\
                                    Fraction_Carbon ,\
                                    Rotura          ,\
                                    RoturaBending
import numpy as np
import pandas as pd
nu = 0.4

theta = lambda x: 0.5 + 0.5*np.tanh(100*x)
relu  = lambda x: x*theta(x)

def objetive(radius,tn,tl,En,El,Sl,df,ni,give_pred=False,factor={"t":1,
                                                                 "St":1,
                                                                 "Sb":1,
                                                                 "Et":1,
                                                                 "Eb":1,
                                                                 "Vc":1}):

    t_p = Tau_model(tn, tl, ni)


    Et_p =  [E_Tensile(En, El, tn, tl, ilayer ) 
             for ilayer in df["layers"]]
    Et_p = np.array(Et_p)

    Eb_p =  [E_flexion(En, El, tn, tl, ilayer ) 
             for ilayer in df["layers"]]

    Vc = [ Fraction_Carbon(radius,tn,tl,ilayer) 
            for ilayer in df["layers"]]

    St = [ Rotura(c,Et_p[i],El,Sl) 
            for i,c in enumerate(df["layers"])]
    # 
    # En este caso cambiamos Et_p -> Eb_p
    # Parece que el modulo de flexión produce mejores resultados
    # en la comparación analítico vs FEM
    #
    Sb = [ RoturaBending(c,Eb_p[i],El,Sl,tn,tl) 
            for i,c in enumerate(df["layers"])]

    error_t   = 100*abs(df["t [mm]"]   - t_p )/df["t [mm]"]
    error_Et  = 100*abs(df["Et [GPa]"] - Et_p)/df["Et [GPa]"]
    error_Eb  = 100*abs(df["Eb [GPa]"] - Eb_p)/df["Eb [GPa]"]
    error_St  = 100*abs(df["St [MPa]"] - St  )/df["St [MPa]"]
    error_Sb  = 100*abs(df["Sb [MPa]"] - Sb  )/df["Sb [MPa]"]
    error_Vc  = 100*abs(df["Vc"]      - Vc )/df["Vc"]

    if give_pred:
        pred_df = pd.DataFrame({
            "t [mm]"  : t_p,
            "Et [GPa]": Et_p,
            "Eb [GPa]": Eb_p,
            "St [MPa]": St,
            "Sb [MPa]": Sb,
            "Vc"      : Vc   
        })

        error_df = pd.DataFrame({
            "t [%]"  : error_t,
            "Et [%]": error_Et,
            "Eb [%]": error_Eb,
            "Vc [%]": error_Vc,
            "St [%]": error_St,
            "Sb [%]": error_Sb
        })
        return pred_df, error_df
    else:

        L_t  = (error_t**2).mean()
        L_Et = (error_Et**2).mean()
        L_Eb = (error_Eb**2).mean()
        L_Vc = (error_Vc**2).mean()
        L_St = (error_St**2).mean()
        L_Sb = (error_Sb**2).mean()

    
        # return  L_t + L_Eb + L_Et  + L_Vc
        L_mul = 1e3*relu(En - np.min(El))

        return L_t  * factor["t"]  + \
               L_Eb * factor["Eb"] + \
               L_Et * factor["Et"] + \
               L_Vc * factor["Vc"] + \
               L_St * factor["St"] + \
               L_Sb * factor["Sb"] + \
               L_mul