from validation.TensileExperimental import TensileExperimental
from validation.BendingExperimental import BendingExperimental
import pandas as pd

def FullExperimental():

    r_Tensile = TensileExperimental()
    r_Bending = BendingExperimental()

    df_s_t = r_Tensile["df_stats"]
    df_s_b = r_Bending["df_stats"]

    t_t = df_s_t["t [mm]"].values
    t_b = df_s_b["t [mm]"].values
    t_mean = (t_t + t_b) / 2

    col_remove = ["t [mm]", 
                "ni",
                "v [X,SX,Y,SY]", 
                "layers"]
    for col in col_remove:
        df_s_t.pop(col)


    # add the bending data to the tensile data Eb [GPa]
    df_s = pd.concat([df_s_t, df_s_b], axis=1)

    df_s.rename(columns={"v [X,SX,Y,SY]": "delta"}, inplace=True)
    df_s = df_s.drop(columns=["delta","ni"],level=0)
    df_s["t [mm]"] = t_mean


    V_carbon_exp = [0.178,
                    0.164,
                    0.135,
                    0.144,
                    0.146,
                    0.180]
    
    df_s["Vc"] = V_carbon_exp

    return df_s