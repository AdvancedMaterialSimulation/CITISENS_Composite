from validation.get_vector import get_vector
import numpy as np

# =============================================================================
def Tau_model(tn, tl, ni):
    return tn + 2*tl*ni

# =============================================================================
def E_Tensile(En,El,tn,tl,layers,omega=1):

    delta = get_vector(layers)
    ni  = len(layers)
    tt = Tau_model(tn, tl, ni)
    E_eff = omega*(En*tn + 2*tl*np.dot(delta,El))/tt
    return E_eff

# =============================================================================

El_dict = { "X" :None, 
            "SX":None, 
            "Y" :None, 
            "SY":None}
    
def E_flexion(En,El,tn,tl,layers,gamma=1.0):

    El_dict["X"]  = El[0]
    El_dict["SX"] = El[1]
    El_dict["Y"]  = El[2]
    El_dict["SY"] = El[3]

    El_s = [ El_dict[ily] for ily in layers] 
    
    ni = len(El_s)
    tt = Tau_model(tn, tl, ni)
 
    rng = np.arange(1,ni+1)    # [1,2,3,...,ni]
    rng = rng - 0.5            # [0.5, 1.5 , 2.5,...,ni-0.5]
    Yg = tn/2 +  tl*rng        # [Yg1, Yg2, Yg3,...,Ygni]

    Il = (1/12)*tl**3 + tl*Yg**2
    In = (1/12)*tn**3
    It = (1/12)*tt**3
     
    return gamma*(En*In + 2*np.dot(El_s,Il))/It

# =============================================================================

longs = { "X": 60.0,
          "Y": 60.0,
          "SX": 31.830988618379067,
          "SY": 31.830988618379067 }

def Fraction_Carbon(radius,tn,tl,layers):

    A_RVE = 10*10 # mm^2

    ni = len(layers)
    tt = Tau_model(tn,tl,ni)
    v_tol = tt*A_RVE

    A_Section = np.pi * radius**2 # mm^2
    v_car = 2*A_Section*np.sum([ longs[ily] for ily in layers ])

    return v_car/v_tol

# =============================================================================

longs = { "X": 60.0,
          "Y": 60.0,
          "SX": 31.830988618379067,
          "SY": 31.830988618379067 }

radius = { "X": 0.5,
            "Y": 0.5,
            "SX": 0.5,
            "SY": 0.5 }

def Fraction_Carbon_2(rr,tn,tl,layers):

    radius["X"] = rr[0]
    radius["SX"] = rr[1]
    radius["Y"] = rr[2]
    radius["SY"] = rr[3]

    A_RVE = 10*10 # mm^2

    ni = len(layers)
    tt = Tau_model(tn,tl,ni)
    v_tol = tt*A_RVE

    v_car = 2*np.sum([ np.pi * radius[ily]**2*longs[ily] for ily in layers ])

    return v_car/v_tol
# =============================================================================

El_dict = { "X" :None, 
            "SX":None, 
            "Y" :None, 
            "SY":None}

Sl_dict = { "X" :None,
            "SX":None,
            "Y" :None,
            "SY":None}

def Rotura(layers,E_eff,El,sigmal,gamma=1.0):

    El_dict["X"]  = El[0]
    El_dict["SX"] = El[1]
    El_dict["Y"]  = El[2]
    El_dict["SY"] = El[3]

    El_s = np.array([ El_dict[ily] for ily in layers] )


    Sl_dict["X"]  = sigmal[0]
    Sl_dict["SX"] = sigmal[1]
    Sl_dict["Y"]  = sigmal[2]
    Sl_dict["SY"] = sigmal[3]

    Sl_s = np.array([ Sl_dict[ily] for ily in layers] )

    return np.min(E_eff*Sl_s/El_s)

El_dict = { "X" :None, 
            "SX":None, 
            "Y" :None, 
            "SY":None}

Sl_dict = { "X" :None,
            "SX":None,
            "Y" :None,
            "SY":None}
# =============================================================================
def RoturaBending(layers,E_eff,El,sigmal,tn,tl):

    El_dict["X"]  = El[0]
    El_dict["SX"] = El[1]
    El_dict["Y"]  = El[2]
    El_dict["SY"] = El[3]

    Ei_s = np.array([ El_dict[ily] for ily in layers] )


    Sl_dict["X"]  = sigmal[0]
    Sl_dict["SX"] = sigmal[1]
    Sl_dict["Y"]  = sigmal[2]
    Sl_dict["SY"] = sigmal[3]


    ni = len(Ei_s)
    tt = Tau_model(tn, tl, ni)
    rng = np.arange(1,ni+1)    # [1,2,3,...,ni]
    #rng = rng - 0.5            # [0.5, 1.5 , 2.5,...,ni-0.5]
    Yg = tn/2 +  tl*rng        # [Yg1, Yg2, Yg3,...,Ygni] 

    Sl_s = np.array([ Sl_dict[ily] for ily in layers] )
    Y_max = tt/2

    return np.min(Sl_s*(E_eff/Ei_s)*(Y_max/Yg))

