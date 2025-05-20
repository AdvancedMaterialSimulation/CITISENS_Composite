from AnalyticalLayers.models import Tau_model       ,\
                                    E_flexion       ,\
                                    E_Tensile       ,\
                                    Rotura          ,\
                                    RoturaBending
import numpy as np
import pandas as pd
nu = 0.4

theta = lambda x: 0.5 + 0.5*np.tanh(100*x)
relu  = lambda x: x*theta(x)

def objetive(tn,tl,En,El,Sl,df,ni,give_pred=False,factor={"t":1,
                                                                 "St":1,
                                                                 "Sb":1,
                                                                 "Et":1,
                                                                 "Eb":1,
                                                                 "Vc":1}):

    t_p = Tau_model(tn, tl, ni)


    Et_p =  [E_Tensile(En, El, tn, tl, ilayer,omega=1.0)  
             for ilayer in df["layers"]]
    Et_p = np.array(Et_p)

    Eb_p =  [E_flexion(En, El, tn, tl, ilayer,gamma=1.0 ) 
             for ilayer in df["layers"]]


    St = [ Rotura(c,Et_p[i],El,Sl,gamma=1.0) 
            for i,c in enumerate(df["layers"])]
    # 
    # En este caso cambiamos Et_p -> Eb_p
    # Parece que el modulo de flexión produce mejores resultados
    # en la comparación analítico vs FEM
    #
    Sb = [ RoturaBending(c,Eb_p[i],El,Sl,tn,tl) 
            for i,c in enumerate(df["layers"])]

    error_Et  = 100*abs(df["Et [GPa]"] - Et_p)/df["Et [GPa]"]
    error_Eb  = 100*abs(df["Eb [GPa]"] - Eb_p)/df["Eb [GPa]"]
    error_St  = 100*abs(df["St [MPa]"] - St  )/df["St [MPa]"]
    error_Sb  = 100*abs(df["Sb [MPa]"] - Sb  )/df["Sb [MPa]"]

    if give_pred:
        pred_df = pd.DataFrame({
            "Et [GPa]": Et_p,
            "Eb [GPa]": Eb_p,
            "St [MPa]": St,
            "Sb [MPa]": Sb,
        })

        error_df = pd.DataFrame({
            "Et [%]": error_Et,
            "Eb [%]": error_Eb,
            "St [%]": error_St,
            "Sb [%]": error_Sb
        })

        pred_df.index = df.index
        return pred_df, error_df
    else:

        L_Et = (error_Et**2).mean()
        L_Eb = (error_Eb**2).mean()
        L_St = (error_St**2).mean()
        L_Sb = (error_Sb**2).mean()

    
        # return  L_t + L_Eb + L_Et  + L_Vc
        L_mul = 1e3*relu(En - np.min(El))

        return L_Eb * factor["Eb"] + \
               L_Et * factor["Et"] + \
               L_St * factor["St"] + \
               L_Sb * factor["Sb"] + \
               L_mul