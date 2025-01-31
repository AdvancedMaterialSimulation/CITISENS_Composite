
import numpy as np
def circle(r):


    trajs =[]  
    # =============================================================================

    nq = 2
    fc1 = lambda x: (r**nq - x**nq)**(1/nq)

    x12 = np.linspace(0,r,2000)
    y12 = fc1(x12)
    z12 = np.zeros_like(x12) 

    trajs.append( np.array([x12,y12,z12]).T )
    # =============================================================================

    nq = 2
    fc1 = lambda x: -(r**nq - (x-2*r)**nq)**(1/nq) + 2*r

    x12 = np.linspace(r,2*r,2000)
    y12 = fc1(x12)
    z12 = np.zeros_like(x12) 

    trajs.append( np.array([x12,y12,z12]).T )

    return trajs

def sincos(r):


    trajs =[]  
    # =============================================================================

    fc1 = lambda x: r*np.cos(0.5*np.pi*x/r)

    x12 = np.linspace(0,r,5000)
    y12 = fc1(x12)

    trajs.append( np.array([x12,y12, np.zeros_like(x12)]).T )

    # =============================================================================

    fc1 = lambda x: r*np.cos(0.5*np.pi*x/r) + 2*r
    # 
    x12 = np.linspace(r,2*r,5000)
    y12 = fc1(x12)
    # 
    trajs.append( np.array([x12,y12, np.zeros_like(x12)]).T )

    return trajs
    # ==================

def sincos_sm(r):

    trajs =[]  
    # =========================================

    fc1 = lambda x: 0.5*r*np.cos(0.5*np.pi*x/r)

    x12 = np.linspace(0,r,5000)
    y12 = fc1(x12)

    trajs.append( np.array([x12,y12, np.zeros_like(x12)]).T )

    # ==========================================

    fc1 = lambda x: 0.5*r*np.cos(0.5*np.pi*x/r) + 2*r
    # 
    x12 = np.linspace(r,2*r,5000)
    y12 = fc1(x12)
    # 
    trajs.append( np.array([x12,y12, np.zeros_like(x12)]).T )

    return trajs
    # ==================