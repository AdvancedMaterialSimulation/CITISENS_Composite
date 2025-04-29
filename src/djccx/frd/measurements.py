import numpy as np

def compute_von_misses(SXX, SYY, SZZ, SXY, SXZ, SYZ):
    return np.sqrt(0.5 * ( (SXX - SYY)**2 +
                           (SYY - SZZ)**2 + 
                           (SZZ - SXX)**2 + 
                           6 * (SXY**2 + SXZ**2 + SYZ**2) ))

def von_misses(frd):
    for ifrd in frd["data_blocks"]:
        S_von_mises = compute_von_misses(ifrd["SXX"], ifrd["SYY"], ifrd["SZZ"],
                                        ifrd["SXY"], ifrd["SZX"], ifrd["SYZ"])
        ifrd["S_von_mises"] = S_von_mises

def principal_stress(frd):
    for ifrd in frd["data_blocks"]:
        SXX = ifrd["SXX"].values
        SYY = ifrd["SYY"].values
        SZZ = ifrd["SZZ"].values
        SXY = ifrd["SXY"].values
        SXZ = ifrd["SZX"].values
        SYZ = ifrd["SYZ"].values
        matrix = [ np.array([[ SXX[i], SXY[i], SXZ[i] ],
                            [ SXY[i], SYY[i], SYZ[i] ],
                            [ SXZ[i], SYZ[i], SZZ[i] ]]) 
                            for i in range(len(SXX)) ]
        # 
        matrix = np.array(matrix)
        autovalores = np.linalg.eigvals(matrix)
        # sort eigenvalues
        autovalores = np.sort(autovalores, axis=1)
        # flip eigenvalues
        autovalores = np.flip(autovalores, axis=1)

        ifrd["P1"] = autovalores[:,0]
        ifrd["P2"] = autovalores[:,1]
        ifrd["P3"] = autovalores[:,2]
