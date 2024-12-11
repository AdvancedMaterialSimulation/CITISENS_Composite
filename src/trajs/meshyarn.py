from trajs.transform import transform
from trajs.uniform import uniform
import numpy as np
from scipy.interpolate import NearestNDInterpolator
# deep copy
import copy
def meshyarn(trajs,ry,N=100):

    yarns = []
    for t1 in trajs:
        t1 = uniform(t1)
        dt1 = np.diff(t1, axis=0)

        samples = np.arange(0, t1.shape[0], N)
        t1_sample  =  t1[samples]
        dt1_sample = dt1[samples]
        # add last 
        t1_sample = np.vstack((t1_sample, t1[-1]))
        dt1_sample = np.vstack((dt1_sample, dt1[-1]))

        disks = []
        for i in range(len(t1_sample)):
            vec_z = dt1_sample[i]
            vec_x = np.array([0,0,1])
            xms, yms, zms = transform(vec_x,vec_z,t1_sample[i],ry)

            disks.append({
                "disk": np.array([xms, yms, zms]),
                "vec_z": vec_z
            })

        yarns.append({
            "disks": disks,
            "traj": t1,
            "traj_sample": t1_sample,
        })

    return yarns


def frd2yarns(yarns,frd):

# interpolar resultados 

    xvalues = frd["x"]
    yvalues = frd["y"]
    zvalues = frd["z"]
    fvalues = frd["P1"]

    interp = NearestNDInterpolator(list(zip(xvalues, yvalues, zvalues)),
                                            fvalues)

    yarns = copy.deepcopy(yarns)
    for j in range(len(yarns)):
        yarn = yarns[j]
        disks = yarn["disks"]
        for i in range(len(disks)):
            disk = disks[i]["disk"]
            disks[i]["P1"] = interp(disk.T)
            disks[i]["P1_mu"] = np.mean(disks[i]["P1"])

        yarns[j]["P1"] = np.array([disk["P1_mu"] for disk in disks])
        yarns[j]["P1_max"] = np.max(yarns[j]["P1"])

    return yarns


def frdsteps2yarns(yarns,frd):

    results = []
    frd_steps = frd["data_blocks"]
    for i in range(len(frd_steps)):
        yarns = frd2yarns(yarns,frd_steps[i])
        results.append({
            "step": frd["steps"][i],
            "yarns": yarns,
            "P1_max": np.max([yarn["P1_max"] for yarn in yarns])
        })

    return results
