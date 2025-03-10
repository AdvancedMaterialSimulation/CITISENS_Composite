from validation.get_vector import get_vector
import numpy as np

# =============================================================================
tl_dict = {"X":None, "Y":None, "SX":None, "SY":None}
El_dict = {"X":None, "Y":None, "SX":None, "SY":None}
def Tau_model(layers,tn, tl):

    tl_dict["X"]  = tl[0]
    tl_dict["SX"] = tl[1]
    tl_dict["Y"]  = tl[2]
    tl_dict["SY"] = tl[3]

    tl_s = [ tl_dict[ilayer] for ilayer in layers]    
    return tn + 2*np.sum(tl_s)

# =============================================================================
def E_Tensile(En,El,tn,tl,layers):

    tl_dict["X"]  = tl[0]
    tl_dict["SX"] = tl[1]
    tl_dict["Y"]  = tl[2]
    tl_dict["SY"] = tl[3]

    tl_s = [ tl_dict[ilayer] for ilayer in layers]    

    El_dict["X"]  = El[0]
    El_dict["SX"] = El[1]
    El_dict["Y"]  = El[2]
    El_dict["SY"] = El[3]

    El_s = [ El_dict[ilayer] for ilayer in layers]

    tt = Tau_model(layers,tn, tl)
    E_eff = (En*tn + 2*np.dot(tl_s,El_s))/tt
    return E_eff

# =============================================================================

    
def E_flexion(En,El,tn,tl,layers):

    El_dict["X"]  = El[0]
    El_dict["SX"] = El[1]
    El_dict["Y"]  = El[2]
    El_dict["SY"] = El[3]

    El_s = [ El_dict[ily] for ily in layers] 

    # 
    tl_dict["X"]  = tl[0]
    tl_dict["SX"] = tl[1]
    tl_dict["Y"]  = tl[2]
    tl_dict["SY"] = tl[3]

    tl_s = [ tl_dict[ilayer] for ilayer in layers] 
    tl_s = np.array(tl_s)   
    # 
    tt = Tau_model(layers,tn, tl)
    #
    # t1/2
    # t1 + t2/2
    # t1 + t2 + t3/2
    # t1 + t2 + t3 + t4/2
    Yg_rng = []
    for i in range(len(layers)):
        Yg_rng.append( tl_s[i]/2 + np.sum(tl_s[:i]) )
    Yg_rng = np.array(Yg_rng)
    
    Yg = tn/2 +  Yg_rng        # [Yg1, Yg2, Yg3,...,Ygni]

    Il = (1/12)*tl_s**3 + tl_s*Yg**2
    In = (1/12)*tn**3
    It = (1/12)*tt**3
    
    return (En*In + 2*np.dot(El_s,Il))/It

# =============================================================================

longs = { "X": 70.0,
          "Y": 70.0,
          "SX": 40.0,
          "SY": 40.0 }

def Fraction_Carbon(radius,tn,tl,layers):

    A_RVE = 10*10 # mm^2

    tt = Tau_model(layers,tn, tl)

    v_tol = tt*A_RVE

    A_Section = np.pi * radius**2 # mm^2
    v_car = 2*A_Section*np.sum([ longs[ily] for ily in layers ])

    return v_car/v_tol