
import numpy as np

eq_vec = lambda p1,p2: np.linalg.norm(np.array(p2) - np.array(p1)) < 1e-4
inside = lambda points_ext,r0: np.sum([ eq_vec(r0[:2],ip) for ip in points_ext] ) != 0

def is_semicylinder_mesh(itraj,Lx,Ly):

    is_line = np.sum(np.std(itraj,axis=0) < 1e-4) == 2

    r0 = itraj[0]

    points_ext = [ 
        [0  , 0  ],
        [0  , Ly ],
        [Lx , Ly ],
        [Lx , 0  ]
    ]

    in_ext = inside(points_ext,r0)

    if is_line and in_ext:
        return True
    else:
        return False
